import logging
from functools import partial
from typing import Dict, Any

from aiomcache import Client
from asphalt.core import Component, Context, merge_config
from typeguard import check_argument_types

logger = logging.getLogger(__name__)


class MemcachedComponent(Component):
    """
    Publishes one or more :class:`aiomcache.Client` resources.

    If ``clients`` is given, a Memcached client resource will be published for each key in the
    dictionary, using the key as the resource name. Any extra keyword arguments to the component
    constructor will be used as defaults for omitted configuration values.

    If ``clients`` is omitted, a single Memcached client resource (``default`` / ``ctx.memcached``)
    is published using any extra keyword arguments passed to the component.

    The client(s) will not connect to the target server until they're used for the first time.

    :param clients: a dictionary of resource name ⭢ :meth:`configure_client` arguments
    :param default_client_args: default values for omitted :meth:`configure_client` arguments
    """

    def __init__(self, clients: Dict[str, Dict[str, Any]] = None, **default_client_args):
        assert check_argument_types()
        if not clients:
            default_client_args.setdefault('context_attr', 'memcached')
            clients = {'default': default_client_args}

        self.clients = []
        for resource_name, config in clients.items():
            config = merge_config(default_client_args, config or {})
            config.setdefault('context_attr', resource_name)
            context_attr, client = self.configure_client(**config)
            self.clients.append((resource_name, context_attr, client))

    @classmethod
    def configure_client(cls, context_attr: str, host: str = 'localhost', port: int = 11211,
                         **client_args):
        """
        Configure a Memcached client.

        :param context_attr: context attribute of the serializer (if omitted, the resource name
            will be used instead)
        :param host: host name or ip address to connect to
        :param port: port number to connect to
        :param client_args: extra keyword arguments passed to :class:`aiomcache.Client`

        """
        assert check_argument_types()
        client = Client(host, port, **client_args)
        return context_attr, client

    @staticmethod
    async def shutdown_client(event, client, resource_name):
        client.close()
        logger.info('Memcached client (%s) shut down', resource_name)

    async def start(self, ctx: Context):
        for resource_name, context_attr, client in self.clients:
            ctx.finished.connect(
                partial(self.shutdown_client, client=client, resource_name=resource_name))
            ctx.publish_resource(client, resource_name, context_attr)
            logger.info('Configured Memcached client (%s / ctx.%s)', resource_name, context_attr)

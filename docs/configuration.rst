Configuration
-------------

.. highlight:: yaml

The typical Memcached configuration using a single server at ``localhost`` on the default port,
database 0 would look like this::

    components:
      memcached:

The above configuration creates a :class:`aiomcache.Client` instance in the context, available as
``ctx.memcached`` (resource name: ``default``).

If you wanted to connect to port 10000 on ``192.168.0.9``, you would do::

    components:
      memcached:
        host: 192.168.0.9
        port: 10000

A more complex configuration creating two :class:`~aiomcache.Client` instances might look like::

    components:
      memcached:
        clients:
          mc1:
            host: 192.168.0.9
          mc2:
            host: 192.168.0.10
            port: 11212

This configuration creates two :class:`~aiomcache.Client` resources, ``mc1`` and ``mc2``
(``ctx.mc1`` and ``ctx.mc2``) respectively.

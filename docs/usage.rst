Using the Memcached client
==========================

The wrapped aiomcache library unfortunately does not have any published documentation, so you will
have to resort to reading the docstrings in the source code of the `aiomcache.Client`_ class.

The following snippet sets a key named ``somekey`` and then retrieves the key and makes sure the
value matches::

    async def handler(ctx):
        await ctx.memcached.set(b'somekey', b'somevalue')
        assert await ctx.memcached.get(b'somekey') == b'somevalue'


.. _aiomcache.Client: https://github.com/aio-libs/aiomcache/blob/master/aiomcache/client.py

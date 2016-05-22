import pytest
from aiomcache import Client

from asphalt.core import Context
from asphalt.memcached.component import MemcachedComponent


@pytest.mark.asyncio
async def test_default_connection(caplog):
    """Test that the default connection is started and is available on the context."""
    async with Context() as context:
        await MemcachedComponent().start(context)
        assert isinstance(context.memcached, Client)

    records = [record for record in caplog.records if record.name == 'asphalt.memcached.component']
    records.sort(key=lambda r: r.message)
    assert len(records) == 2
    assert records[0].message == "Configured Memcached client (default / ctx.memcached)"
    assert records[1].message == 'Memcached client (default) shut down'


@pytest.mark.asyncio
async def test_multiple_connections(caplog):
    """Test that a multiple connection configuration works as intended."""
    async with Context() as context:
        await MemcachedComponent(clients={
            'mc1': {'host': '1.2.3.4', 'port': 11212},
            'mc2': {'host': '127.0.0.2'}
        }).start(context)
        assert isinstance(context.mc1, Client)
        assert isinstance(context.mc2, Client)

    records = [record for record in caplog.records if record.name == 'asphalt.memcached.component']
    records.sort(key=lambda r: r.message)
    assert len(records) == 4
    assert records[0].message == 'Configured Memcached client (mc1 / ctx.mc1)'
    assert records[1].message == 'Configured Memcached client (mc2 / ctx.mc2)'
    assert records[2].message == 'Memcached client (mc1) shut down'
    assert records[3].message == 'Memcached client (mc2) shut down'

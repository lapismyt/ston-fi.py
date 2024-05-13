from pytoniq import LiteBalancer, Address
from stonfi import RouterV1, PoolV1, PTON_V1_ADDRESS
import pytest
import asyncio

router = RouterV1()

PTON = Address(PTON_V1_ADDRESS)
BOLT = Address('EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw')

TON_BOLT_POOL_ADDR = Address('EQAa4jR_TLCE0X3OQZJknsU3dFBccDVclCzmSjpR6aRNAIuy')
TON_BOLT_POOL = PoolV1(TON_BOLT_POOL_ADDR)


@pytest.mark.asyncio
async def test_get_pool_address():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    pool_address: Address = await router.get_pool_address(PTON, BOLT, provider)
    state = await provider.get_account_state(pool_address)
    await provider.close_all()
    assert state.is_active()
    assert pool_address == TON_BOLT_POOL_ADDR

@pytest.mark.asyncio
async def test_get_pool():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    pool: PoolV1 = await router.get_pool(PTON, BOLT, provider)
    state = await provider.get_account_state(pool.address)
    await provider.close_all()
    assert state.is_active()
    assert pool == TON_BOLT_POOL

@pytest.mark.asyncio
async def test_get_data():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    data = await router.get_data(provider)
    await provider.close_all()
    print(data)

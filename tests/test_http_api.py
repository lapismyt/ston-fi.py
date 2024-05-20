import pytest
import asyncio
from stonfi.http import HTTPAPI

http_api = HTTPAPI()


@pytest.mark.asyncio
async def test_get_assets():
    assets = await http_api.get_assets()
    assert assets is not None
    assert len(assets) > 0
    print('First asset: ', assets[0].display_name)


@pytest.mark.asyncio
async def test_get_farms():
    farms = await http_api.get_farms()
    assert farms is not None
    assert len(farms) > 0
    print('First farm pool address: ', farms[0].pool_address)


@pytest.mark.asyncio
async def test_get_markets():
    markets = await http_api.get_markets()
    assert markets is not None
    assert len(markets) > 0
    print('First pair: ', markets[0])


@pytest.mark.asyncio
async def test_get_pools():
    pools = await http_api.get_pools()
    assert pools is not None
    assert len(pools) > 0
    print('First pool address: ', pools[0].address)


@pytest.mark.asyncio
async def test_swap_simulate():
    swap_simulate = await http_api.swap_simulate(
        offer_address='EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA',
        ask_address='EQCM3B12QK1e4yZSf8GtBRT0aLMNyEsBc_DhVfRRtOEffLez',
        units='300',
        slippage_tolerance=0.01,
    )
    print('Swap rate: ', swap_simulate.swap_rate)


@pytest.mark.asyncio
async def test_reverse_swap_simulate():
    simulate = await http_api.reverse_swap_simulate(
        offer_address='EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA',
        ask_address='EQCM3B12QK1e4yZSf8GtBRT0aLMNyEsBc_DhVfRRtOEffLez',
        units='300',
        slippage_tolerance=0.01,
    )
    print('Reverse Swap rate: ', simulate.swap_rate)


@pytest.mark.asyncio
async def test_get_swap_status():
    status = await http_api.get_swap_status(
        router_address='EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt',
        owner_address='EQCM3B12QK1e4yZSf8GtBRT0aLMNyEsBc_DhVfRRtOEffLez',
        query_id=1,
    )
    print('Status: ', status.type)


@pytest.mark.asyncio
async def test_jetton_wallet_address():
    address = await http_api.get_jetton_wallet_address(
        'EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt',
        'EQB5Wjo7yXdaB70yBoN2YEv8iVPjAdMObf_Dq40ELLaPllNb'
    )
    print('Address: ', address.to_str(is_user_friendly=True))


@pytest.mark.asyncio
async def test_get_jetton_wallet_address():
    address = await http_api.get_jetton_wallet_address(
        'EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt',
        'EQB5Wjo7yXdaB70yBoN2YEv8iVPjAdMObf_Dq40ELLaPllNb'
    )
    print('Jetton address: ', address.to_str(is_user_friendly=True))


@pytest.mark.asyncio
async def test_get_wallet_assets():
    assets = await http_api.get_wallet_assets("EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt")
    assert assets is not None
    assert len(assets) > 0
    print('First asset balance: ', int(assets[0].balance) / 1e9, assets[0].display_name)


@pytest.mark.asyncio
async def test_get_wallet_farms():
    farm = await http_api.get_wallet_farms("EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt")
    assert farm is not None
    assert len(farm) > 0
    print('First farm pool address: ', farm[0].pool_address)

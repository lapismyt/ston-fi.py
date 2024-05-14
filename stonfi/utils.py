from stonfi import HTTPAPI, PoolV1
import asyncio
from pytoniq import Address, LiteClientLike
from async_lru import alru_cache

@alru_cache
async def get_jetton_decimals(jetton_address: str | Address) -> int | None:
    http_api = HTTPAPI()
    jetton_address = jetton_address.to_str() if isinstance(jetton_address, Address) else jetton_address
    assets = await http_api.get_assets()
    for asset in assets['asset_list']:
        if asset['contract_address'] == jetton_address:
            return asset['decimals']
    return None

async def get_pool_readiness(pool: PoolV1, provider: LiteClientLike):
    state = await provider.get_account_state(pool.address)
    if not state.is_active():
        return False
    data = await pool.get_data(provider)
    for x in ['reserve0', 'reserve1']:
        if not data[x] > 0:
            return False
    return True


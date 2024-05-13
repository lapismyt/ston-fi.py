from stonfi import HTTPAPI
import asyncio
from pytoniq import Address

async def get_jetton_decimals(jetton_address: str | Address) -> int:
    http_api = HTTPAPI()
    jetton_address = jetton_address.to_str() if isinstance(jetton_address, Address) else jetton_address
    assets = await http_api.get_assets()
    for asset in assets['asset_list']:
        if asset['contract_address'] == jetton_address:
            return asset['decimals']
    return None
import aiohttp
from pytoniq import Address
import asyncio
import traceback

class HTTPAPI:
    def __init__(self,
                 base_url: str = 'https://api.ston.fi/'):
        self.base_url = base_url.rstrip('/')
    
    async def get(self, path: str, **kwargs):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.base_url + path, params=kwargs) as resp:
                        if resp.content_type != 'application/json':
                            result = {'exit_code': 'swap_ok'}
                        else:
                            result = await resp.json()
                break
            except:
                traceback.print_exc()
                await asyncio.sleep(0.5)
        return result
    
    async def post(self, path: str, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url + path, json=kwargs) as resp:
                result = await resp.json()
        return result
    
    async def get_assets(self):
        return await self.get('/v1/assets')
    
    async def get_farms(self):
        return await self.get('/v1/farms')
    
    async def get_markets(self):
        return await self.get('/v1/markets')
    
    async def get_pools(self):
        return await self.get('/v1/pools')
    
    async def simulate_swap(self,
                            offer_address: str | Address,
                            ask_address: str | Address,
                            units: int | str,
                            slippage_tolerance: float = 0.01,
                            referral_address: str | Address | None = None):
        return await self.post('/v1/swap/simulate',
                               offer_address=offer_address.to_str() if isinstance(offer_address, Address) else offer_address,
                               ask_address=ask_address.to_str() if isinstance(ask_address, Address) else ask_address,
                               units=str(units),
                               slippage_tolerance=str(round(slippage_tolerance * 100, 3)),
                               referral_address=referral_address.to_str() if isinstance(referral_address, Address) else referral_address)
    
    async def get_swap_status(self,
                              router_address: str | Address,
                              owner_address: str | Address,
                              query_id: int | str):
        return await self.get(f'/v1/swap/status',
                               router_address=router_address.to_str() if isinstance(router_address, Address) else router_address,
                               owner_address=owner_address.to_str() if isinstance(owner_address, Address) else owner_address,
                               query_id=str(query_id))
    
    async def get_jetton_wallet_address(self,
                                        owner_address: str | Address,
                                        addr_str: str | Address):
        return await self.get(f'/v1/jetton/{addr_str.to_str() if isinstance(addr_str, Address) else addr_str}/address',
                               owner_address=owner_address.to_str() if isinstance(owner_address, Address) else owner_address)
    
    async def get_wallet_assets(self,
                                addr_str: str | Address):
        return await self.get(f'/v1/wallets/{addr_str.to_str() if isinstance(addr_str, Address) else addr_str}/assets')
    
    async def get_wallet_farms(self,
                                addr_str: str | Address):
        return await self.get(f'/v1/wallets/{addr_str.to_str() if isinstance(addr_str, Address) else addr_str}/farms')
    
    # TODO: /v1/wallets/{addr_str}/operations
    # TODO: /v1/wallets/{addr_str}/pools
    # TODO: /v1/stats/dex
    # TODO: /v1/stats/operations
    # TODO: /v1/stats/pool
    # TODO: /export/cmc/v1
    
    async def close(self):
        await self.session.close()


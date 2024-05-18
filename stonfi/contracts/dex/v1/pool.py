from pytoniq import begin_cell, Cell, Address, LiteClientLike, Slice
from stonfi.constants import OP, GAS
from stonfi.contracts.jetton.jetton_root import JettonRoot
from stonfi.contracts.jetton.jetton_wallet import JettonWallet
from typing import Optional, Union, Type

class PoolV1:
    def __init__(self, address: Address):
        self.address = address
    
    def __eq__(self, other: Type['PoolV1']) -> bool:
        return self.address == other.address

    @staticmethod
    async def create_collect_fees_body(query_id: int = 0):
        return begin_cell()\
                .store_uint(OP.COLLECT_FEES, 32)\
                .store_uint(query_id, 64)\
                .end_cell()
    
    async def build_collect_fees_tx_params(self,
                                           gas_amount: int = GAS.POOL.COLLECT_FEES,
                                           query_id: int = 0):
        return {
            'to': self.address,
            'payload': await self.create_collect_fees_body(query_id),
            'gas_amount': gas_amount
        }

    @staticmethod
    async def create_burn_body(amount: int,
                               response_address: Union[Address, str],
                               query_id: int = 0):
        return begin_cell()\
                .store_uint(OP.REQUEST_BURN, 32)\
                .store_uint(query_id, 64)\
                .store_coins(amount)\
                .store_address(response_address)\
                .end_cell()
    
    async def build_burn_tx_params(self,
                                   amount: int,
                                   response_address: Union[Address, str],
                                   provider: LiteClientLike,
                                   gas_amount: int = GAS.POOL.BURN,
                                   query_id: int = 0):
        to: JettonWallet = await JettonRoot(self.address).get_wallet(response_address, provider)
        payload = await self.create_burn_body(amount, to.address, query_id)

        return {
            'to': to.address,
            'payload': payload,
            'gas_amount': gas_amount
        }
    
    async def get_expected_outputs(self,
                                   amount: int,
                                   jetton_wallet: Union[Address, str],
                                   provider: LiteClientLike):
        jetton_wallet = Address(jetton_wallet) if isinstance(jetton_wallet, str) else jetton_wallet
        stack = await provider.run_get_method(self.address,
                                              'get_expected_outputs',
                                              [amount,
                                              jetton_wallet.to_cell().begin_parse()])
        
        return {
            'jetton_to_receive': stack[0],
            'protocol_fee_paid': stack[1],
            'ref_fee_paid': stack[2]
        }
    
    async def get_expected_tokens(self,
                                  amount0: int,
                                  amount1: int,
                                  provider: LiteClientLike):
        stack = await provider.run_get_method(self.address,
                                              'get_expected_tokens',
                                              [amount0,
                                              amount1])
        return stack[0]
    
    async def get_expected_liquidity(self,
                                     jetton_amount: int,
                                     provider: LiteClientLike):
        stack = await provider.run_get_method(self.address,
                                              'get_expected_liquidity',
                                              [jetton_amount])
        return {
            'amount0': stack[0],
            'amount1': stack[1]
        }
    
    async def get_lp_account_address(self,
                                     owner_address: Union[Address, str],
                                     provider: LiteClientLike):
        
        stack: list[Slice] = await provider.run_get_method(self.address,
                                                           'get_lp_account_address',
                                                           [owner_address.to_cell().begin_parse()])
        return stack[0].load_address()
    
    async def get_jetton_wallet(self,
                                owner_address: Union[Address, str],
                                provider: LiteClientLike):
        return await JettonRoot(self.address).get_wallet(owner_address, provider)
    
    async def get_data(self, provider: LiteClientLike):
        stack: list[Union[int, Slice, Cell]] = await provider.run_get_method(self.address, 'get_pool_data', [])
        return {
            'reserve0': stack[0],
            'reserve1': stack[1],
            'token0_wallet_address': stack[2].load_address(),
            'token1_wallet_address': stack[3].load_address(),
            'lp_fee': stack[4],
            'protocol_fee': stack[5],
            'ref_fee': stack[6],
            'protocol_fee_address': stack[7].load_address(),
            'collected_token0_protocol_fee': stack[8],
            'collected_token1_protocol_fee': stack[9]
        }
    
    async def get_lp_account(self,
                             owner_address: Union[Address, str],
                             provider: LiteClientLike):
        raise NotImplementedError()


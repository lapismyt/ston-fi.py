from pytoniq import begin_cell, Cell, Address, LiteClientLike, Slice
from stonfi.constants import ROUTER_V1_ADDRESS, OP, GAS, PTON_V1_ADDRESS
from stonfi.contracts.pTON.v1 import pTON_V1
from stonfi.contracts.jetton.jetton_root import JettonRoot
from stonfi.contracts.jetton.jetton_wallet import JettonWallet
from stonfi.contracts.dex.v1.pool import PoolV1
from typing import Optional, Union

class RouterV1:
    def __init__(self, address = ROUTER_V1_ADDRESS):
        self.address = Address(address)

    @staticmethod
    async def create_swap_body(user_wallet_address: Union[Address, str],
                               min_ask_amount: int,
                               ask_jetton_wallet_address: Union[Address, str],
                               referral_address: Optional[Union[Address, str]] = None):
        body = begin_cell()\
                .store_uint(OP.SWAP, 32)\
                .store_address(ask_jetton_wallet_address)\
                .store_coins(min_ask_amount)\
                .store_address(user_wallet_address)\
                .store_address(referral_address)
        
        if referral_address is None:
            body = body.store_uint(0, 1)
        else:
            body = body.store_uint(1, 1)\
                    .store_address(referral_address)

        return body.end_cell()

    async def _build_swap(self,
                          user_wallet_address: Union[Address, str],
                          offer_jetton_address: Union[Address, str],
                          ask_jetton_address: Union[Address, str],
                          offer_amount: int,
                          min_ask_amount: int,
                          provider: LiteClientLike,
                          referral_address: Optional[Union[Address, str]] = None,
                          gas_amount: Optional[int] = GAS.JETTON_TO_JETTON.GAS_AMOUNT,
                          forward_gas_amount: Optional[
                              int] = GAS.JETTON_TO_JETTON.FORWARD_GAS_AMOUNT,
                          query_id: Optional[int] = 0,
                          offer_owner_address=None):

        if not offer_owner_address:
            offer_owner_address = self.address

        offer_jetton_wallet: JettonWallet = await JettonRoot(offer_jetton_address).get_wallet(offer_owner_address, provider)
        ask_jetton_wallet: JettonWallet = await JettonRoot(ask_jetton_address).get_wallet(self.address, provider)

        forward_payload = await self.create_swap_body(user_wallet_address=user_wallet_address,
                                                      min_ask_amount=min_ask_amount,
                                                      ask_jetton_wallet_address=ask_jetton_wallet.address,
                                                      referral_address=referral_address)

        payload = offer_jetton_wallet.create_transfer_payload(destination=self.address,
                                                              amount=offer_amount,
                                                              query_id=query_id,
                                                              response_address=user_wallet_address,
                                                              forward_amount=forward_gas_amount,
                                                              forward_payload=forward_payload)
        return {
            'to': offer_jetton_wallet.address.to_str(),
            'payload': payload,
            'amount': gas_amount
        }

    async def build_swap_jetton_to_jetton_tx_params(self,
                                                    user_wallet_address: Union[Address, str],
                                                    offer_jetton_address: Union[Address, str],
                                                    ask_jetton_address: Union[Address, str],
                                                    offer_amount: int,
                                                    min_ask_amount: int,
                                                    provider: LiteClientLike,
                                                    referral_address: Optional[Union[Address, str]] = None,
                                                    gas_amount: Optional[int] = GAS.JETTON_TO_JETTON.GAS_AMOUNT,
                                                    forward_gas_amount: Optional[int] = GAS.JETTON_TO_JETTON.FORWARD_GAS_AMOUNT,
                                                    query_id: Optional[int] = 0):
        return await self._build_swap(
            user_wallet_address=user_wallet_address,
            offer_jetton_address=offer_jetton_address,
            ask_jetton_address=ask_jetton_address,
            offer_amount=offer_amount,
            min_ask_amount=min_ask_amount,
            provider=provider,
            referral_address=referral_address,
            gas_amount=gas_amount,
            forward_gas_amount=forward_gas_amount,
            query_id=query_id,
            offer_owner_address=user_wallet_address
        )

    async def build_swap_jetton_to_ton_tx_params(self,
                                                 user_wallet_address: Union[Address, str],
                                                 offer_jetton_address: Union[Address, str],
                                                 offer_amount: int,
                                                 min_ask_amount: int,
                                                 provider: LiteClientLike,
                                                 proxy_ton_address: Union[Address, str] = PTON_V1_ADDRESS,
                                                 referral_address: Optional[Union[Address, str]] = None,
                                                 gas_amount: Optional[int] = GAS.JETTON_TO_TON.GAS_AMOUNT,
                                                 forward_gas_amount: Optional[int] = GAS.JETTON_TO_TON.FORWARD_GAS_AMOUNT,
                                                 query_id: Optional[int] = 0):
        
        return await self._build_swap(
                    user_wallet_address=user_wallet_address,
                    offer_jetton_address=offer_jetton_address,
                    ask_jetton_address=proxy_ton_address,
                    offer_amount=offer_amount,
                    min_ask_amount=min_ask_amount,
                    provider=provider,
                    referral_address=referral_address,
                    gas_amount=gas_amount,
                    forward_gas_amount=forward_gas_amount,
                    query_id=query_id,
                    offer_owner_address=user_wallet_address)
    
    async def build_swap_ton_to_jetton_tx_params(self,
                                                user_wallet_address: Union[Address, str],
                                                ask_jetton_address: Union[Address, str],
                                                offer_amount: int,
                                                min_ask_amount: int,
                                                provider: LiteClientLike,
                                                proxy_ton_address: Union[Address, str] = PTON_V1_ADDRESS,
                                                referral_address: Optional[Union[Address, str]] = None,
                                                forward_gas_amount: Optional[int] = GAS.TON_TO_JETTON.FORWARD_GAS_AMOUNT,
                                                query_id: Optional[int] = 0):

        return await self._build_swap(
            user_wallet_address=user_wallet_address,
            offer_jetton_address=proxy_ton_address,
            ask_jetton_address=ask_jetton_address,
            offer_amount=offer_amount,
            min_ask_amount=min_ask_amount,
            provider=provider,
            referral_address=referral_address,
            gas_amount=forward_gas_amount + offer_amount,
            forward_gas_amount=forward_gas_amount,
            query_id=query_id,
        )

    @staticmethod
    async def create_provide_liquidity_body(router_wallet_address: Union[Address, str],
                                            min_lp_out: int):
        return begin_cell()\
                .store_uint(OP.PROVIDE_LIQUIDITY, 32)\
                .store_address(router_wallet_address)\
                .store_coins(min_lp_out)\
                .end_cell()

    async def build_provide_liquidity_jetton_tx_params(self,
                                                       user_wallet_address: Union[Address, str],
                                                       send_token_address: Union[Address, str],
                                                       other_token_address: Union[Address, str],
                                                       send_amount: int,
                                                       min_lp_out: int,
                                                       provider: LiteClientLike,
                                                       gas_amount: int = GAS.LP_JETTON.GAS_AMOUNT,
                                                       forward_gas_amount: int = GAS.LP_JETTON.FORWARD_GAS_AMOUNT,
                                                       query_id: int = 0):
        jetton_wallet_address: JettonWallet = await JettonRoot(send_token_address).get_wallet(user_wallet_address, provider)
        router_wallet_address: JettonWallet = await JettonRoot(other_token_address).get_wallet(self.address, provider)

        forward_payload = await self.create_provide_liquidity_body(router_wallet_address = router_wallet_address.address,
                                                                   min_lp_out = min_lp_out)
        
        payload = jetton_wallet_address.create_transfer_payload(destination = self.address,
                                                              amount = send_amount,
                                                              query_id = query_id,
                                                              response_address = user_wallet_address,
                                                              forward_amount = forward_gas_amount,
                                                              forward_payload = forward_payload)
        
        return {
            'to': jetton_wallet_address.address.to_str(),
            'payload': payload,
            'amount': gas_amount
        }

    async def build_provide_liquidity_ton_tx_params(self,
                                                    user_wallet_address: Union[Address, str],
                                                    other_token_address: Union[Address, str],
                                                    send_amount: int,
                                                    min_lp_out: int,
                                                    provider: LiteClientLike,
                                                    proxy_ton_address: Optional[Union[Address, str]] = PTON_V1_ADDRESS,
                                                    forward_gas_amount: Optional[int] = GAS.LP_TON.FORWARD_GAS_AMOUNT,
                                                    query_id: int = 0):
        proxy_ton_wallet: JettonWallet = await JettonRoot(proxy_ton_address).get_wallet(self.address, provider)
        router_wallet: JettonWallet = await JettonRoot(other_token_address).get_wallet(self.address, provider)

        forward_payload = await self.create_provide_liquidity_body(router_wallet_address = router_wallet.address,
                                                                   min_lp_out = min_lp_out)
        
        payload = proxy_ton_wallet.create_transfer_payload(destination = self.address,
                                                           amount = send_amount,
                                                           query_id = query_id,
                                                           response_address = user_wallet_address,
                                                           forward_amount = forward_gas_amount,
                                                           forward_payload = forward_payload)
        
        return {
            'to': proxy_ton_wallet.address.to_str(),
            'payload': payload,
            'amount': send_amount + forward_gas_amount
        }
    
    async def get_pool_address(self,
                               jetton0: Union[Address, str],
                               jetton1: Union[Address, str],
                               provider: LiteClientLike):
        jetton0_wallet_address: Address = (await JettonRoot.create_from_address(jetton0).get_wallet(self.address, provider)).address
        jetton1_wallet_address: Address = (await JettonRoot.create_from_address(jetton1).get_wallet(self.address, provider)).address
        stack: list[Slice] = await provider.run_get_method(self.address,
                                                           'get_pool_address',
                                                           [jetton0_wallet_address.to_cell().begin_parse(),
                                                            jetton1_wallet_address.to_cell().begin_parse()])
        return stack[0].load_address()
    
    async def get_pool(self,
                       jetton0: Union[Address, str],
                       jetton1: Union[Address, str],
                       provider: LiteClientLike):
        return PoolV1(await self.get_pool_address(jetton0, jetton1, provider))
    
    async def get_data(self, provider: LiteClientLike):
        stack: list[Union[Slice, Cell]] = await provider.run_get_method(self.address, 'get_router_data', [])
        result = {
            'is_locked': bool(stack[0]),
            'admin_address': stack[1].load_address(),
            'temp_upgrade': stack[2],
            'pool_code': stack[3],
            'jetton_lp_wallet_code': stack[4],
            'lp_account_code': stack[5]
        }
        return result

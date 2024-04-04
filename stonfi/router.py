from tonsdk.boc import begin_cell, Cell
from tonsdk.utils import Address
from tonsdk.utils import to_nano, from_nano
from typing import Optional
from stonfi.ton import ToncenterClient
from stonfi import utils
from decimal import Decimal

class OP_CODE:
    SWAP = 0x25938561

class GAS_CONST:
    SWAP = 0.3
    SWAP_FORWARD = 0.265

class Router:
    def __init__(self,
                 client: ToncenterClient,
                 address: str = 'EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt'):
        self.address = Address(address)
        self.client = client

    def _maybe_to_addr(self, address: str | Address | None):
        if address is None:
            return None
        if not isinstance(address, Address):
            return Address(address)
        return address

    
    def create_swap_body(self,
                         user_wallet_address: str | Address,
                         min_ask_amount: int | float,
                         ask_jetton_wallet_address: str | Address,
                         referral_address: Optional[str | Address] = None) -> Cell:
        user_wallet_address = self._maybe_to_addr(user_wallet_address)
        ask_jetton_wallet_address = self._maybe_to_addr(ask_jetton_wallet_address)
        referral_address = self._maybe_to_addr(referral_address)

        payload = begin_cell()\
                    .store_uint(OP_CODE.SWAP, 32)\
                    .store_address(ask_jetton_wallet_address)\
                    .store_coins(to_nano(min_ask_amount, 'ton'))\
                    .store_address(user_wallet_address)
        
        if referral_address is not None:
            payload = payload.store_uint(1, 1)\
                                .store_address(referral_address)
        else:
            payload = payload.store_uint(0, 1)

        return payload.end_cell()
    

    def build_swap_jetton_tx_params(self,
                                    user_wallet_address: str | Address,
                                    offer_jetton_address: str | Address,
                                    ask_jetton_address: str | Address,
                                    offer_amount: str | Address,
                                    min_ask_amount: int | float,
                                    gas_amount: Optional[int | float] = None,
                                    forward_gas_amount: Optional[int | float] = None,
                                    referral_address: Optional[str | Address] = None,
                                    query_id: Optional[int] = None) -> Cell:
        user_wallet_address = self._maybe_to_addr(user_wallet_address)
        offer_jetton_address = self._maybe_to_addr(offer_jetton_address)
        ask_jetton_address = self._maybe_to_addr(ask_jetton_address)
        referral_address = self._maybe_to_addr(referral_address)

        offer_jetton_wallet = self.client.get_jetton_wallets(owner_address = user_wallet_address.to_string(True, True, True),
                                                            jetton_address = offer_jetton_address.to_string(True, True, True),
                                                            limit = 1)['jetton_wallets'][0]
        offer_jetton_wallet_address = self._maybe_to_addr(offer_jetton_wallet['address'])
            
        ask_jetton_wallet = self.client.get_jetton_wallets(owner_address = self.address.to_string(True, True, True),
                                                           jetton_address = ask_jetton_address.to_string(True, True, True),
                                                           limit = 1)['jetton_wallets'][0]
        ask_jetton_wallet_address = self._maybe_to_addr(ask_jetton_wallet['address'])

        forward_payload = self.create_swap_body(user_wallet_address = user_wallet_address,
                                                min_ask_amount = min_ask_amount,
                                                ask_jetton_wallet_address = ask_jetton_wallet_address,
                                                referral_address = referral_address)
        
        if forward_gas_amount is None:
            forward_ton_amount = to_nano(GAS_CONST.SWAP_FORWARD, 'ton')
        else:
            forward_ton_amount = forward_gas_amount
        
        if gas_amount is None:
            gas_amount = to_nano(GAS_CONST.SWAP, 'ton')

        if query_id is None:
            query_id = 0
        
        payload = utils.create_jetton_transfer_body(to_address = ask_jetton_wallet_address,
                                                      jetton_amount = to_nano(offer_amount, 'ton'),
                                                      forward_amount = forward_ton_amount,
                                                      forward_payload = forward_payload,
                                                      response_address = offer_jetton_wallet_address,
                                                      query_id = query_id)
        
        return {'to': offer_jetton_wallet_address.to_string(True, True, True),
                'payload': payload,
                'amount': from_nano(gas_amount, 'ton')}
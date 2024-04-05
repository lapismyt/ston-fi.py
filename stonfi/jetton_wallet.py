from tonsdk.contract.token.ft import JettonWallet
from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell
from typing import Union, Optional

class JettonWallet(JettonWallet):

    @classmethod
    def create_transfer_payload(
        cls,
        destination: Union[Address, str],
        amount: int,
        query_id: int = 0,
        response_address: Union[Address, None] = None,
        custom_payload: Union[Cell, None] = None,
        forward_amount: int = 0,
        forward_payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0xf8a7ea5, 32)\
            .store_uint(query_id, 64)\
            .store_coins(amount)\
            .store_address(destination)\
            .store_address(response_address)\
            .store_maybe_ref(custom_payload)\
            .store_coins(forward_amount)\
            .store_maybe_ref(forward_payload)\
            .end_cell()
from tonsdk.utils import to_nano, from_nano
import requests
import json
from typing import Optional
from pytoniq import Address
from stonfi.jetton_wallet import JettonWallet
import time

# TEST_MNEMONICS = ['side', 'topic', 'eight', 'smile', 'banner', 'muffin', 'various', 'remind', 'ketchup', 'narrow', 'future', 'nuclear', 'tobacco', 'shoulder', 'fire', 'pulse', 'genuine', 'scissors', 'alcohol', 'lady', 'divorce', 'suffer', 'thunder', 'good']

def get_seqno(client, address):
    resp = client.run_get_method(address, "seqno")
    try:
        seqno = int(resp["stack"][0]["value"], 16)
    except KeyError as err:
        print(repr(err))
        print(resp)
        raise err
    return seqno

def get_balance(client, address):
    balance = int(client.get_account_info(address)["balance"])
    if balance <= 0:
        return 0.0
    else:
        return from_nano(balance, 'ton')

# def create_jetton_transfer_body(destination: Address,
#                                 jetton_amount: int,
#                                 forward_amount: Optional[int] = 0,
#                                 forward_payload: Optional[Cell] = None,
#                                 custom_payload: Optional[Cell] = None,
#                                 response_address: Optional[Address] = None,
#                                 query_id: Optional[int] = 0) -> Cell:
#     payload = begin_cell()\
#                 .store_uint(0xf8a7ea5, 32)\
#                 .store_uint(query_id, 64)\
#                 .store_coins(jetton_amount)\
#                 .store_address(destination)\
#                 .store_address(response_address)\
#                 .store_maybe_ref(custom_payload)\
#                 .store_coins(forward_amount)\
#                 .store_maybe_ref(forward_payload)\
#                 .end_cell()
#     return payload

create_jetton_transfer_body = JettonWallet.create_transfer_payload
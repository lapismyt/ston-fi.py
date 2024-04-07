from tonsdk.utils import to_nano, from_nano
import requests
import json
from typing import Optional
from tonsdk.utils import Address
from stonfi.jetton_wallet import JettonWallet
import time
import decimal
from stonfi.ton import ToncenterClient

# TEST_MNEMONICS = ['side', 'topic', 'eight', 'smile', 'banner', 'muffin', 'various', 'remind', 'ketchup', 'narrow', 'future', 'nuclear', 'tobacco', 'shoulder', 'fire', 'pulse', 'genuine', 'scissors', 'alcohol', 'lady', 'divorce', 'suffer', 'thunder', 'good']

def maybe_to_addr(address: str | Address | None):
    if address is None:
        return None
    if not isinstance(address, Address):
        return Address(address)
    return address

def to_nano(number: int | float, client: ToncenterClient, unit: Optional[str | Address] = 'ton'):
    if isinstance(unit, Address):
        unit_addr = maybe_to_addr(unit)
    elif unit.lower() == 'ton':
        return int(number * (10 ** 9))
    jetton_masters = client.get_jetton_masters(address = unit_addr.to_string(True, True, True), limit = 1)
    if not 'jetton_masters' in jetton_masters:
        raise ValueError('Wrong response')
    jetton_masters = jetton_masters['jetton_masters']
    if len(jetton_masters) == 0:
        raise KeyError('Jetton not found')
    content = jetton_masters[0]['jetton_content']
    if 'decimals' in content:
        decimals == int(content['decimals'])
    else:
        decimals = 9
    return int(number * (10 ** decimals))

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
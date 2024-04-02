from tonsdk.utils import to_nano, from_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
import requests
import json
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
        return balance / 10**9
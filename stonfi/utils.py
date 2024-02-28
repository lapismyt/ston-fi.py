from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.provider import ToncenterClient
import requests
import json
import time

TEST_MNEMONICS = ['side', 'topic', 'eight', 'smile', 'banner', 'muffin', 'various', 'remind', 'ketchup', 'narrow', 'future', 'nuclear', 'tobacco', 'shoulder', 'fire', 'pulse', 'genuine', 'scissors', 'alcohol', 'lady', 'divorce', 'suffer', 'thunder', 'good']

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

def create_wallet(client, deploy_wallet=None, testnet=False, init_amount=0.1):
    wallet_tuple = Wallets.create(version=WalletVersionEnum.v3r2, workchain=0)
    mnemonics = wallet_tuple[0]
    priv_k = wallet_tuple[1]
    pub_k = wallet_tuple[2]
    wallet = wallet_tuple[3]
    if deploy_wallet is None and testnet == True:
        dep_wallet_tuple = Wallets.from_mnemonics(mnemonics=TEST_MNEMONICS, version=WalletVersionEnum.v3r2, workchain=0)
        dep_mnemonics = dep_wallet_tuple[0]
        dep_priv_k = dep_wallet_tuple[1]
        dep_pub_k = dep_wallet_tuple[2]
        deploy_wallet = dep_wallet_tuple[3]
    elif deploy_wallet is None:
        raise Exception("Deploy wallet is None")
    else:
        pass
    if testnet == True:
        try:
            wallet_address = wallet.address.to_string(True, True, False, True)
            deploy_wallet_address = deploy_wallet.address.to_string(True, True, True, True)
        except AttributeError as err:
            print(repr(err))
            print(wallet)
            print(deploy_wallet)
    else:
        wallet_address = wallet.address.to_string(True, True, False)
        deploy_wallet_address = deploy_wallet.address.to_string(True, True, True)
    seqno = get_seqno(client, deploy_wallet_address)
    query = deploy_wallet.create_transfer_message(to_addr=wallet_address, amount=to_nano(init_amount, "ton"), seqno=seqno)
    message = query["message"].to_boc(False)
    data = client.send_message(message)
    balance = 0
    while balance <= 0:
        time.sleep(1)
        balance = get_balance(client, wallet_address)
    query = wallet.create_init_external_message()
    message = query["message"].to_boc(False)
    client.send_message(message)
    return wallet

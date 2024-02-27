from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from pytonlib import TonlibClient
import requests
from pathlib import Path
import json
import asyncio

TEST_MNEMONICS = mnemonics = ['side', 'topic', 'eight', 'smile', 'banner', 'muffin', 'various', 'remind', 'ketchup', 'narrow', 'future', 'nuclear', 'tobacco', 'shoulder', 'fire', 'pulse', 'genuine', 'scissors', 'alcohol', 'lady', 'divorce', 'suffer', 'thunder', 'good']

async def create_client(testnet=False, ls_index=2, keystore_dir="/tmp/ton_keystore", tonlib_timeout=15):
    if testnet:
        url = "https://ton.org/testnet-global.config.json"
    else:
        url == "https://ton.org/global-config.json"
    config = requests.get(url).json()
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)
    client = TonlibClient(ls_index=ls_index, config=config, keystore=keystore_dir, tonlib_timeout=tonlib_timeout)
    await client.init()
    return client

async def get_seqno(client, address):
    resp = await client.raw_run_method(method="seqno", stack_data=[], address=address)
    seqno = int(resp["stack"][0][1], 16)
    return seqno

async def get_balance(client, address):
    balance = int((await client.raw_get_account_state(address))["balance"])
    if balance <= 0:
        return 0.0
    else:
        return balance / 10**9

async def create_wallet(client, deploy_wallet=None, testnet=False):
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
    seqno = await get_seqno(client, deploy_wallet_address)
    query = deploy_wallet.create_transfer_message(to_addr=wallet_address, amount=to_nano(0.03, "ton"), seqno=seqno)
    message = query["message"].to_boc(False)
    data = await client.raw_send_message(message)
    balance = 0
    while balance <= 0:
        await asyncio.sleep(3)
        balance = await get_balance(client, wallet_address)
        print(balance)
    query = wallet.create_init_external_message()
    message = query["message"].to_boc(False)
    await client.raw_send_message(message)
    return wallet

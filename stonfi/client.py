from tonsdk.contract.token.ft import JettonWallet
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from stonfi.ton import ToncenterClient
from stonfi.utils import get_seqno
from tonsdk.boc import begin_cell, Cell, Slice
from tonsdk.utils import Address, to_nano, from_nano
import random
import codecs
import json

class StonFiClient(ToncenterClient):
    OP_SWAP = 0x25938561
    OP_REQUEST_TRANSFER = 0xf8a7ea5
    GAS_NANO = to_nano(0.3, "ton")
    STONFI_ADDR = "EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt"
    
    def create_swap_body(self,
                         user_wallet: Address,
                         ask_jetton_wallet: Address,
                         min_ask_amount: int,
                         referral_address: Address | None = None):
        print(5)
        print(ask_jetton_wallet, user_wallet, referral_address, sep="\n")
        cell = begin_cell()\
                .store_uint(self.OP_SWAP, 32)\
                .store_address(ask_jetton_wallet)\
                .store_coins(min_ask_amount)\
                .store_address(user_wallet)
        print(6)
        if referral_address is None:
            cell = cell.store_uint(1, 1)\
                    .store_address(referral_address)
        else:
            cell = cell.store_uint(0, 1)
        print(7)
        return Slice(cell.end_cell()).read_string().encode()

    def create_swap_jetton_message(self,
                                    user_wallet: Address,
                                    min_ask_amount: int,
                                    ask_jetton: Address,
                                    offer_jetton: Address,
                                    offer_amount: int,
                                    referral_address: Address | None = None):
        print(2)
        ask_jetton_wallets = self.get_jetton_wallets(
            owner_address=self.STONFI_ADDR,
            jetton_address=ask_jetton.to_string(True, True, True),
            limit=1
        )["jetton_wallets"]
        ask_jetton_wallet = Address(ask_jetton_wallets[0]["address"])
        print(3)

        offer_jetton_wallets = self.get_jetton_wallets(
            owner_address=user_wallet.to_string(),
            jetton_address=offer_jetton.to_string(True, True, True),
            limit=1
        )["jetton_wallets"]
        offer_jetton_wallet = Address(offer_jetton_wallets[0]["address"])
        print(4)

        swap_body = self.create_swap_body(
            user_wallet,
            ask_jetton_wallet,
            min_ask_amount,
            referral_address
        )
        print(8)
        print(9)
        
        payload = JettonWallet().create_transfer_body(
            to_address = ask_jetton_wallet,
            jetton_amount = offer_amount,
            forward_amount = self.GAS_NANO,
            forward_payload = swap_body
        )
        print(10)

        return payload

    def swap(self,
             mnemonics: str | list,
             offer_jetton: str | Address,
             ask_jetton: str | Address,
             offer_amount: int | float,
             min_ask_amount: int | float,
             referral_address: str | Address | None = None):

        if isinstance(mnemonics, str):
            mnemonics = mnemonics.strip().split()
        if isinstance(offer_jetton, str):
            offer_jetton = Address(offer_jetton)
        if isinstance(ask_jetton, str):
            ask_jetton = Address(ask_jetton)
        if isinstance(referral_address, str):
            referral_address = Address(referral_address)

        offer_amount = to_nano(offer_amount, "ton")
        min_ask_amount = to_nano(min_ask_amount, "ton")

        wallet = Wallets.from_mnemonics(mnemonics, version=WalletVersionEnum.v4r2, workchain=0)[3]
        print(1)

        payload = self.create_swap_jetton_message(
            user_wallet = wallet.address,
            offer_jetton = offer_jetton,
            ask_jetton = ask_jetton,
            offer_amount = offer_amount,
            min_ask_amount = min_ask_amount,
            referral_address = referral_address
        )
        print(11)

        seqno = get_seqno(self, wallet)
        query = wallet.create_transfer_message(to_addr=self.STONFI_ADDR, amount=to_nano(0.05, "ton"), seqno=seqno, payload=payload)
        print(12)
        message = query["message"].to_boc()
        return self.send_message(message)

from pytoniq import WalletV4R2, LiteBalancer
from tonsdk.utils import to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from stonfi.ton import ToncenterClient
from stonfi.utils import get_seqno
from stonfi.router import Router
import asyncio
from tonsdk.contract.wallet import SendModeEnum


# please, if you are a human, don't use this credentials in personal goals, only for tests
TONCENTER_API_KEY = 'fdd94593d5ef54878d6766c7d8099deec0f08f67e8ac23065cbadcb9bfd31034'
MNEMONICS = ['grant', 'fantasy', 'index', 'flower', 'over', 'glance', 'rain', 'size', 'abandon', 'like', 'pulp', 'aerobic',
             'tuition', 'name', 'cherry', 'hint', 'dentist', 'giant', 'soft', 'aim', 'actual', 'employ', 'science', 'robust']

async def main():
    # litebalancer = LiteBalancer.from_mainnet_config(1)
    # await litebalancer.start_up()

    # wallet = await WalletV4R2.from_mnemonic(provider = litebalancer, mnemonics=MNEMONICS)
    # wallet_address = wallet.address.to_str(True, True, True)
    
    mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(MNEMONICS, WalletVersionEnum.v4r2)
    wallet_address = wallet.address.to_string(True, True, True)

    toncenter = ToncenterClient(api_key=TONCENTER_API_KEY)

    router = Router(toncenter)

    offer_jetton_address = 'EQA2kCVNwVsil2EM2mB0SkXytxCqQjS4mttjDpnXmwG9T6bO' # STON
    ask_jetton_address = 'EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA' # jUSDT

    print(toncenter.get_jetton_wallets(owner_address = wallet_address,
                                       jetton_address = offer_jetton_address,
                                       limit = 1))

    print(toncenter.get_jetton_wallets(owner_address = wallet_address,
                                       jetton_address = ask_jetton_address,
                                       limit = 1))

    swap_params = router.build_swap_jetton_tx_params(user_wallet_address = wallet_address,
                                                    offer_jetton_address = offer_jetton_address,
                                                    ask_jetton_address = ask_jetton_address,
                                                    offer_amount = 0.01,
                                                    min_ask_amount = 0,
                                                    gas_amount = 0.32
                                                    # referral_address = wallet_address
                                                    )

    print(swap_params)

    # response = await wallet.transfer(destination=swap_params['to'],
    #                            amount=swap_params['amount'],
    #                            body=swap_params['payload'],)

    seqno = get_seqno(toncenter, wallet_address)

    message = wallet.create_transfer_message(swap_params['to'],
                                             swap_params['amount'],
                                             seqno,
                                             swap_params['payload'])['message']
    response = toncenter.send_message(message.to_boc(False))
    print(response)

    # await litebalancer.close_all()

if __name__ == '__main__':
    asyncio.run(main())
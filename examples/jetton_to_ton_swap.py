from tonsdk.contract.wallet import Wallets, WalletVersionEnum, SendModeEnum
from stonfi.ton import ToncenterClient
from stonfi.utils import get_seqno
from stonfi.router import Router
from stonfi.router import GAS_CONST
import time

# please, if you are a human, don't use this credentials in personal goals, only for tests. get your Toncenter key in @tonapibot
TONCENTER_API_KEY = 'fdd94593d5ef54878d6766c7d8099deec0f08f67e8ac23065cbadcb9bfd31034'
MNEMONICS = ['grant', 'fantasy', 'index', 'flower', 'over', 'glance', 'rain', 'size', 'abandon', 'like', 'pulp', 'aerobic',
             'tuition', 'name', 'cherry', 'hint', 'dentist', 'giant', 'soft', 'aim', 'actual', 'employ', 'science', 'robust']

def jetton_to_ton_swap():
    
    mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(MNEMONICS, WalletVersionEnum.v4r2)
    wallet_address = wallet.address.to_string(True, True, True)

    toncenter = ToncenterClient(api_key=TONCENTER_API_KEY)

    router = Router(toncenter)
    
    offer_jetton_address = 'EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA' # jUSDT
    proxy_ton_address = 'EQCM3B12QK1e4yZSf8GtBRT0aLMNyEsBc_DhVfRRtOEffLez' # pTON

    print(toncenter.get_jetton_wallets(owner_address = wallet_address,
                                       jetton_address = offer_jetton_address,
                                       limit = 1))

    print(toncenter.get_jetton_wallets(owner_address = wallet_address,
                                       jetton_address = proxy_ton_address,
                                       limit = 1))

    time.sleep(1)

    # known issues:
    # wrong jetton amount with jettons that use not 9 decimals
    swap_params = router.build_swap_jetton_tx_params(user_wallet_address = wallet_address,
                                                    offer_jetton_address = offer_jetton_address,
                                                    ask_jetton_address = proxy_ton_address,
                                                    offer_amount = 0.00001,
                                                    min_ask_amount = 0, # WARNING: use real min_ask_amount or you can lost your Jettons forever
                                                    gas_amount = GAS_CONST.SWAP + 0.025,
                                                    referral_address = 'UQBoWzqvRC6ZbDVMh75An2GCHN98CCljYoOip1qvgpLLB4tv'
                                                    # referral_address = wallet_address
                                                    )

    print(swap_params)

    seqno = get_seqno(toncenter, wallet_address)

    message = wallet.create_transfer_message(swap_params['to'],
                                             swap_params['amount'],
                                             seqno,
                                             swap_params['payload'])['message']
    
    response = toncenter.send_message(message.to_boc(False))
    print(response)

if __name__ == '__main__':
    jetton_to_ton_swap()
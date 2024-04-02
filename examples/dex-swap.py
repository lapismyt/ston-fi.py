from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from stonfi.ton import ToncenterClient
from stonfi.utils import get_seqno
from stonfi.router import Router

TONCENTER_API_KEY = 'fdd94593d5ef54878d6766c7d8099deec0f08f67e8ac23065cbadcb9bfd31034'
MNEMONICS = ['grant', 'fantasy', 'index', 'flower', 'over', 'glance', 'rain', 'size', 'abandon', 'like', 'pulp', 'aerobic',
             'tuition', 'name', 'cherry', 'hint', 'dentist', 'giant', 'soft', 'aim', 'actual', 'employ', 'science', 'robust']

mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(MNEMONICS, WalletVersionEnum.v4r2)
wallet_address = wallet.address.to_string(True, True, True)

client = ToncenterClient(api_key=TONCENTER_API_KEY)

router = Router(client)

offer_jetton_address = 'EQA2kCVNwVsil2EM2mB0SkXytxCqQjS4mttjDpnXmwG9T6bO' # STON
ask_jetton_address = 'EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA' # jUSDT

print(client.get_jetton_wallets(owner_address = wallet_address,
                                jetton_address = offer_jetton_address,
                                limit = 1))

print(client.get_jetton_wallets(owner_address = wallet_address,
                                jetton_address = ask_jetton_address,
                                limit = 1))

swap_params = router.build_swap_jetton_tx_params(user_wallet_address = wallet_address,
                                                 offer_jetton_address = offer_jetton_address,
                                                 ask_jetton_address = ask_jetton_address,
                                                 offer_amount = 0.1,
                                                 min_ask_amount = 0.017,
                                                 referral_address = wallet_address) # BitString Overflow

print(swap_params)


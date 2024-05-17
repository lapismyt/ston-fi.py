import os
import pytest

from pytoniq import Address, WalletV4R2, LiteBalancer
from stonfi import RouterV1
from stonfi.constants import ROUTER_ADDRESS_TESTNET, PTON_ADDRESS_TESTNET

router = RouterV1(address=ROUTER_ADDRESS_TESTNET)
TEST_JETTON = Address('kQBi0fzBTtCfwF1xM6tXMydpJlzfVgtgRmCFx3G--9hx97tM')
TEST_JETTON2 = Address('kQCw3IIGAqo0EylOjMcF8VYs09ikS_F_tV1VnWVgRPAsYl4T')

@pytest.mark.asyncio
async def test_swap_ton_to_jetton():
    if not os.getenv('SEED'):
        raise Exception('[!] Seed phrase not find on env')

    provider = LiteBalancer.from_testnet_config(2)
    await provider.start_up()

    wallet: WalletV4R2 = await WalletV4R2.from_mnemonic(provider, os.getenv('SEED').split())

    params = await router.build_swap_ton_to_jetton_tx_params(
        user_wallet_address=wallet.address,
        ask_jetton_address=TEST_JETTON,
        offer_amount=round(0.2 * 1e9),
        min_ask_amount=1,
        provider=provider,
        proxy_ton_address=PTON_ADDRESS_TESTNET
    )

    resp = await wallet.transfer(
        params['to'],
        params['amount'],
        params['payload']
    )

    await provider.close_all()
    assert resp == 1


@pytest.mark.asyncio
async def test_swap_jetton_to_ton():
    if not os.getenv('SEED'):
        raise Exception('[!] Seed phrase not find on env')

    provider = LiteBalancer.from_testnet_config(2)
    await provider.start_up()

    wallet: WalletV4R2 = await WalletV4R2.from_mnemonic(provider, os.getenv('SEED').split())

    params = await router.build_swap_jetton_to_ton_tx_params(
        user_wallet_address=wallet.address,
        offer_jetton_address=TEST_JETTON,
        offer_amount=int(30*1e9),
        min_ask_amount=1,
        provider=provider,
        proxy_ton_address=PTON_ADDRESS_TESTNET,
    )

    resp = await wallet.transfer(
        params['to'],
        params['amount'],
        params['payload']
    )

    await provider.close_all()
    assert resp == 1


@pytest.mark.asyncio
async def test_swap_jetton_to_jetton():
    if not os.getenv('SEED'):
        raise Exception('[!] Seed phrase not find on venv')

    provider = LiteBalancer.from_testnet_config(2)
    await provider.start_up()

    wallet: WalletV4R2 = await WalletV4R2.from_mnemonic(provider, os.getenv('SEED').split())

    params = await router.build_swap_jetton_to_jetton_tx_params(
        user_wallet_address=wallet.address,
        offer_jetton_address=TEST_JETTON,
        ask_jetton_address=TEST_JETTON2,
        offer_amount=int(1000 * 1e9),
        min_ask_amount=1,
        provider=provider,
    )

    resp = await wallet.transfer(
        params['to'],
        params['amount'],
        params['payload']
    )

    await provider.close_all()
    assert resp == 1

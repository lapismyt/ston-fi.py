import os
import pytest

from pytoniq import Address, WalletV4R2, LiteBalancer
from stonfi import RouterV1
from stonfi.constants import ROUTER_ADDRESS_TESTNET, PTON_ADDRESS_TESTNET


router = RouterV1(address=ROUTER_ADDRESS_TESTNET)

TEST_JETTON = Address('kQBi0fzBTtCfwF1xM6tXMydpJlzfVgtgRmCFx3G--9hx97tM')
TEST_JETTON2 = Address('kQCw3IIGAqo0EylOjMcF8VYs09ikS_F_tV1VnWVgRPAsYl4T')


@pytest.mark.asyncio
async def test_add_to_ton_jetton_pool():
    if not os.getenv('SEED'):
        raise Exception('[!] Seed phrase not find on venv')

    provider = LiteBalancer.from_testnet_config(2)
    await provider.start_up()

    wallet: WalletV4R2 = await WalletV4R2.from_mnemonic(provider, os.getenv('SEED').split())

    params = await router.build_provide_liquidity_ton_tx_params(
        user_wallet_address=wallet.address,
        other_token_address=TEST_JETTON,
        send_amount=int(0.1 * 1e9),
        min_lp_out=1,
        provider=provider,
        proxy_ton_address=PTON_ADDRESS_TESTNET,
    )
    msg1 = wallet.create_wallet_internal_message(
        destination=Address(params['to']),
        value=params['amount'],
        body=params['payload']
    )

    params = await router.build_provide_liquidity_jetton_tx_params(
        user_wallet_address=wallet.address,
        other_token_address=PTON_ADDRESS_TESTNET,
        send_token_address=TEST_JETTON,
        send_amount=int(100 * 1e9),
        min_lp_out=1,
        provider=provider,
    )
    msg2 = wallet.create_wallet_internal_message(
        destination=Address(params['to']),
        value=params['amount'],
        body=params['payload']
    )

    status = await wallet.raw_transfer([msg1, msg2])
    await provider.close_all()

    assert status == 1


@pytest.mark.asyncio
async def test_add_to_jetton_jetton_pool():
    if not os.getenv('SEED'):
        raise Exception('[!] Seed phrase not find on venv')

    provider = LiteBalancer.from_testnet_config(2)
    await provider.start_up()

    wallet: WalletV4R2 = await WalletV4R2.from_mnemonic(provider, os.getenv('SEED').split())

    params = await router.build_provide_liquidity_jetton_tx_params(
        user_wallet_address=wallet.address,
        send_token_address=TEST_JETTON,
        other_token_address=TEST_JETTON2,
        send_amount=int(1 * 1e9),
        min_lp_out=1,
        provider=provider,
    )

    msg1 = wallet.create_wallet_internal_message(
        destination=Address(params['to']),
        value=params['amount'],
        body=params['payload']
    )

    params = await router.build_provide_liquidity_jetton_tx_params(
        user_wallet_address=wallet.address,
        send_token_address=TEST_JETTON2,
        other_token_address=TEST_JETTON,
        send_amount=int(1 * 1e9),
        min_lp_out=1,
        provider=provider,
    )

    msg2 = wallet.create_wallet_internal_message(
        destination=Address(params['to']),
        value=params['amount'],
        body=params['payload']
    )

    status = await wallet.raw_transfer([msg1, msg2])
    await provider.close_all()

    assert status == 1

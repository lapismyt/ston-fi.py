from pytoniq import LiteBalancer, Address
from stonfi import RouterV1, PoolV1, PTON_V1_ADDRESS, JettonRoot, JettonWallet
import pytest
import asyncio
import os

router = RouterV1()

PTON = Address(PTON_V1_ADDRESS)
BOLT = Address('EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw')

pool = PoolV1('EQAa4jR_TLCE0X3OQZJknsU3dFBccDVclCzmSjpR6aRNAIuy')

@pytest.mark.asyncio
async def test_get_expected_outputs():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    pton_wallet = await JettonRoot.create_from_address(PTON).get_wallet(router.address, provider)
    pton_wallet_address = pton_wallet.address
    out = await pool.get_expected_outputs(1, pton_wallet_address, provider)
    print(out)
    await provider.close_all()

@pytest.mark.asyncio
async def test_get_expected_tokens():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    pton_wallet = await JettonRoot.create_from_address(PTON).get_wallet(router.address, provider)
    pton_wallet_address = pton_wallet.address
    out = await pool.get_expected_tokens(1000000000, 1000000000, provider)
    print(out)
    await provider.close_all()

@pytest.mark.asyncio
async def test_get_expected_liquidity():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    out = await pool.get_expected_liquidity(1000000000, provider)
    print(out)
    await provider.close_all()

@pytest.mark.asyncio
async def test_get_lp_account_address():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    out = await pool.get_lp_account_address(Address('UQBoWzqvRC6ZbDVMh75An2GCHN98CCljYoOip1qvgpLLB4tv'), provider)
    print(out)
    await provider.close_all()

@pytest.mark.asyncio
async def test_get_jetton_wallet():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    out = await pool.get_jetton_wallet(Address('UQBoWzqvRC6ZbDVMh75An2GCHN98CCljYoOip1qvgpLLB4tv'), provider)
    print(out)
    await provider.close_all()

@pytest.mark.asyncio
async def test_get_data():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    out = await pool.get_data(provider)
    print(out)
    await provider.close_all()
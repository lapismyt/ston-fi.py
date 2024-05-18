import asyncio
import pytest
from pytoniq import Address, WalletV4R2, LiteBalancer, Cell
from stonfi import RouterV1
import os

router = RouterV1()

RAFF = Address('EQCJbp0kBpPwPoBG-U5C-cWfP_jnksvotGfArPF50Q9Qiv9h')

@pytest.mark.asyncio
async def test_swap():
    if not os.getenv('SEED'):
        return None
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()
    wallet: WalletV4R2 = await WalletV4R2.from_mnemonic(provider, os.getenv('SEED').split())
    params = await router.build_swap_ton_to_jetton_tx_params(wallet.address,
                                                             RAFF,
                                                             round(0.16 * 1e9),
                                                             1,
                                                             provider)
    print(params)
    resp = await wallet.transfer(
        params['to'],
        params['amount'],
        params['payload']
    )
    await provider.close_all()
    assert resp == 1


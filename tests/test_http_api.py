import pytest
import asyncio
from stonfi.http import HTTPAPI

@pytest.mark.asyncio
async def test_http_api():
    http_api = HTTPAPI()
    assets = await http_api.get_assets()
    assert assets is not None
    assert len(assets) > 0
    print('First asset: ', assets['asset_list'][0])
    await http_api.close()


from dataclasses import dataclass

from dataclasses_json import CatchAll, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Pool:
    address: str
    collected_token0_protocol_fee: str
    collected_token1_protocol_fee: str
    deprecated: bool
    lp_fee: str
    lp_price_usd: str
    lp_total_supply: str
    lp_total_supply_usd: str
    protocol_fee: str
    protocol_fee_address: str
    ref_fee: str
    reserve0: str
    reserve1: str
    router_address: str
    token0_address: str
    token1_address: str
    apy_7d: str | None = None
    apy_30d: str | None = None
    apy_1d: str | None = None
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class PoolsResponse:
    pool_list: list[Pool]
    unknown_things: CatchAll = None

    @classmethod
    def from_dict(cls, param):
        pass

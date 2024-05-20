from dataclasses import dataclass

from dataclasses_json import CatchAll, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class SwapSimulate:
    ask_address: str
    ask_units: str
    fee_address: str
    fee_percent: str
    fee_units: str
    min_ask_units: str
    offer_address: str
    offer_units: str
    pool_address: str
    price_impact: str
    router_address: str
    slippage_tolerance: str
    swap_rate: str
    unknown_things: CatchAll = None

    @classmethod
    def from_dict(cls, param):
        pass


# @dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class SwapStatus:
    type: str
    address: str | None = None
    balance_deltas: str | None = None
    coins: str | None = None
    exit_code: str | None = None
    logical_time: str | None = None
    query_id: str | None = None
    tx_hash: str | None = None

    # unknown_things: CatchAll = None

    @staticmethod
    def from_dict(obj: dict) -> 'SwapStatus':
        _type = obj.get('@type')
        _address = obj.get("address")
        _balance_deltas = obj.get("balance_deltas")
        _coins = obj.get("coins")
        _exit_code = obj.get("exit_code")
        _logical_time = obj.get("logical_time")
        _query_id = obj.get("query_id")
        _tx_hash = obj.get("tx_hash")
        return SwapStatus(_type, _address, _balance_deltas, _coins, _exit_code, _logical_time, _query_id, _tx_hash)

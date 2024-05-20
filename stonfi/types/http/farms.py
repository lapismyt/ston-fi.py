from dataclasses import dataclass

from dataclasses_json import CatchAll, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class NftInfo:
    unknown_things: CatchAll = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Farm:
    apy: str
    min_stake_duration_s: str
    minter_address: str
    nft_infos: list[NftInfo]
    pool_address: str
    reward_token_address: str
    status: str
    unknown_things: CatchAll = None

    @classmethod
    def schema(cls):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class FarmsResponse:
    farm_list: list[Farm]
    unknown_things: CatchAll = None

    @classmethod
    def from_dict(cls, param):
        pass

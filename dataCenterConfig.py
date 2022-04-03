from dataclasses import dataclass

@dataclass
class DataCenterConfig:
    rows: int 
    slots: int 
    unavailable: int
    pools: int
    servers: int
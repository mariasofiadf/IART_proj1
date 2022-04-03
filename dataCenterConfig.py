from dataclasses import dataclass
from numpy import array
from typing import List, Tuple

@dataclass
class Server:
    slots: int # number of slots server occupies
    capacity: int 

@dataclass
class DataCenterConfig:
    rows: int # number of rows
    slots: int # number of slots per row
    unavailable: List[Tuple] # coordinates of unavailable slots
    pools: int # number of pools
    servers: List[Server] #array with server sizes. len(servers) = number of servers

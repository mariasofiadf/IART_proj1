from dataclasses import dataclass
from numpy import array
from typing import List, Tuple


@dataclass
class Server:
    id: int
    slots: int # number of slots server occupies
    capacity: int 

@dataclass
class DataCenter:
    rows: int # number of rows
    slots: int # number of slots per row
    unavailable: List[Tuple] # coordinates of unavailable slots
    pools: int # number of pools
    servers: List[Server] #array with servers. len(servers) = number of servers

@dataclass
class Solution:
    pools: List[int]
    dataCenter: List[List[int]]
    def deepcopy(self):
        
        return Solution(self.pools.copy(),[row.copy() for row in self.dataCenter])

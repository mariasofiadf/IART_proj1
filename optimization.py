from dataCenterConfig import DataCenterConfig as config
# Pools example [1,0,0,2,1] 
# This means servers 2 and 3 are assigned to pool 0,
# servers 0 and 4 are assigned to pool 1
# and server 3 is assigned to pool 2
pools = []

# dataCenter example [[1,1,1,-2,-1,-1,3,5],
#                     [-1,2,2,4,4,4,-2,0 ]] 
# -1 means slot is available
# -2 means slot is unavailable
# other numbers mean server N is allocated there
dataCenter = [[]]

# config is an object of the class dataCenterConfig defined in dataCenterCOnfig.py
# @dataclass
# class DataCenterConfig:
#     rows: int 
#     slots: int 
#     unavailable: int
#     pools: int
#     servers: int
def randomSolution(config):
    pools = []
    dataCenter = []
    



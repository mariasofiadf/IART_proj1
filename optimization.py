from random import randint
from dataCenter import DataCenter, Server

MAX_ALLOC_TRIES = 100
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

# config is an object of the class DataCenter defined in dataCenterCOnfig.py
# @dataclass
# class DataCenter:
#     rows: int # number of rows
#     slots: int # number of slots per row
#     unavailable: array[int] # coordinates of unavailable slots
#     pools: int # number of pools
#     servers: array[int] #array with server sizes. len(servers) = number of servers

def randomSolution(config: DataCenter):
    pools = []

    # Randomly assign pools to servers
    for i in range(len(config.servers)):
        pools.append(randint(0,config.pools-1))

    dataCenter =[[-1 for r in range(config.slots)] for s in range(config.rows)]

    # Set unavailable slots accordingly
    for coords in config.unavailable:
        print(coords)
        r,s = coords
        dataCenter[r][s] = -2

    for index, server in enumerate(config.servers):
        assigned = False
        tries = 0
        while not assigned and tries < MAX_ALLOC_TRIES:
            tries += 1
            # Get random row and slot
            r = randint(0, config.rows-1)
            s = randint(0, config.slots-1)
            valid = True

            # Check if server fits at slot s in row r
            for i in range(server.slots):
                if(s+i >= config.slots):
                    valid = False
                    break
                if dataCenter[r][s+i] != -1: # -1 means available
                    valid = False

            # If server doesn't fit it won't be valid
            if not valid:
                continue
            
            # If it's valid assign it
            for i in range(server.slots):
                dataCenter[r][s+i] = index

            assigned = True
    return (pools, dataCenter)

unavailable = [(0,0)]
servers = [Server(3,10), Server(3,10), Server(2,5), Server(1,5), Server(1,1)]
rows = 2
slots = 5
pools = 2
config = DataCenter(rows,slots,unavailable,pools,servers)

pools, dataCenter = randomSolution(config)

print("Pools: ", pools)
print("DataCenter: ", dataCenter)



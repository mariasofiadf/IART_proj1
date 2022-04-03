from dataCenter import DataCenter, Server
from random import randint

MAX_ALLOC_TRIES = 100

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

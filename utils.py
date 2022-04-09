from random import randint
from dataCenter import DataCenter, Solution, Server

def assignServer(solution: Solution, config: DataCenter, server: Server, tries: int):
    for i in range(tries):
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
            if solution.dataCenter[r][s+i] != -1: # -1 means available
                valid = False

        # If server doesn't fit it won't be valid
        if not valid:
            continue
        
        # If it's valid, assign it
        for i in range(server.slots):
            solution.dataCenter[r][s+i] = server

        break
    return solution
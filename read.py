from cmath import pi
from random import seed
from typing import Tuple
from dataCenter import Server, DataCenter


def readDataCenter(file_name):
    f = open(file_name, "r")
    unavailable_coord = []
    servers = []
    lines = f.readlines() # Read in all the lines of the file into a list of lines
    
    rows, slots, unavailable, pools, _ = (int(val) for val in lines[0].split()) #Data from first line

    for i in range (1, unavailable +1): # unavailable slots coordenates
        coords = [int(val) for val in lines[i].split()]
        unavailable_coord.append((coords[0], coords[1]))

    for i in range (unavailable +1, len(lines)):# servers size and capacity
        server_values = [int(val) for val in lines[i].split()]
        server = Server(server_values[0], server_values[1])
        servers.append(server)

    return DataCenter(rows, slots, unavailable_coord, pools, servers)


def writeSolution(sol, file_name):
    


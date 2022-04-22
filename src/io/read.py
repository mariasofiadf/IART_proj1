from src.solution.data_center import Server, DataCenter, Solution
from src.solution.solution import randomSolution



def readDataCenter(file_name):
    f = open(file_name, "r")
    unavailable_coord = []
    servers = []
    lines = f.readlines() # Read in all the lines of the file into a list of lines

    rows, slots, unavailable, pools, _ = (int(val) for val in lines[0].split()) #Data from first line

    for i in range (1, unavailable +1): # unavailable slots coordenates
        coords = [int(val) for val in lines[i].split()]
        unavailable_coord.append((coords[0], coords[1]))

    id = 0
    for i in range (unavailable +1, len(lines)):# servers size and capacity
        server_values = [int(val) for val in lines[i].split()]
        server = Server( id,server_values[0], server_values[1])
        servers.append(server)
        id += 1

    return DataCenter(rows, slots, unavailable_coord, pools, servers)


def writeSolution(sol: Solution, file_name):
    f = open(file_name, 'w')
    data_center = sol.dataCenter
    pools = sol.pools
    for server in range(0, len(pools)):
        row_slot_index = [(index, row.index(server)) for index, row in enumerate(data_center) if server in row]
       # line = str(row_slot_index[0][0]) +  str(pools[server]
        if((row_slot_index)):
            line = str(row_slot_index[0][0]) + " " + str(row_slot_index[0][1]) + " " +  str(pools[server])
            f.write(line)
            f.write('\n')
        else:
            f.write("X\n")


dataCenter = readDataCenter("../../data/problem.txt")
print(dataCenter)
sol1 = randomSolution(dataCenter)

print(sol1)
writeSolution(sol1, "../../data/solution.txt")

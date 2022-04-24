import random
from enum import Enum

import numpy as np

from src.solution.data_center import Solution, DataCenter, Server


class Neighbourhood(Enum):
    RMV_SV = 0
    ADD_SV = 1
    MOV_SV_SLOT = 2
    SWTCH_SV_ROW = 3
    SWTCH_SV_POOL = 4


def get_random_neighbour(solution: Solution, modes: [Neighbourhood], config: DataCenter):
    solution_copy = solution.deepcopy()
    mode = random.choice(modes)

    allocated_server_nos = [x for x in set(
        np.array(solution_copy.dataCenter).flatten()) if x >= 0]
    unallocated_servers_nos = [i for i in range(
        len(config.servers)) if i not in allocated_server_nos]

    if mode == Neighbourhood.ADD_SV and len(unallocated_servers_nos) > 0:
        server_no = random.choice(unallocated_servers_nos)
        return assign_server_to_first_available_slot(solution_copy, config.servers[server_no])
    elif len(allocated_server_nos) > 0:
        server_no = random.choice(allocated_server_nos)
        if mode == Neighbourhood.RMV_SV:
            return unassign_server(solution_copy, config.servers[server_no])
        elif mode == Neighbourhood.MOV_SV_SLOT:
            return move_server_inside_row(solution_copy, config.servers[server_no])
        elif mode == Neighbourhood.SWTCH_SV_ROW:
            return move_server_to_different_row(solution_copy, config.servers[server_no])
        elif mode == Neighbourhood.SWTCH_SV_POOL:
            return move_server_to_different_pool(solution_copy, config.servers[server_no])
    return solution


def move_server_inside_row(solution: Solution, server: Server):
    old_slot: int
    for row_no, row in enumerate(solution.dataCenter):
        for slot_no, slot in enumerate(row):
            if slot == server.id:
                old_slot = slot_no
                break  # Stop searching inside row
        else:
            continue  # Next row
        row[old_slot:old_slot + server.slots] = [-1] * server.slots
        for slot_no, slot in enumerate(row):
            if slot_no != old_slot and row[slot_no:slot_no + server.slots] == [-1] * server.slots:
                solution.dataCenter[row_no][slot_no:slot_no + server.slots] = [server.id] * server.slots
                break  # Stop searching inside row
        else:
            return solution  # No other slot
    return solution


def move_server_to_different_row(solution: Solution, server: Server):
    if len(solution.dataCenter) < 2:
        return solution  # No other row

    old_row_no: int
    for row_no, row in enumerate(solution.dataCenter):
        for slot_no, slot in enumerate(row):
            if slot == server.id:
                old_row_no = row_no
                break  # Stop searching inside row
        else:
            continue  # Next row
        break  # Stop searchhing rows
    else:
        return solution  # Not found

    unassign_server(solution, server)
    new_row_no = old_row_no
    while new_row_no == old_row_no:
        new_row_no = random.randint(0, len(solution.dataCenter) - 1)

    for slot_no in range(len(solution.dataCenter[new_row_no])):
        if solution.dataCenter[new_row_no][slot_no:slot_no + server.slots] == [-1] * server.slots:
            solution.dataCenter[new_row_no][slot_no:slot_no + server.slots] = [server.id] * server.slots
            break
    else:
        return solution

    return solution


def move_server_to_different_pool(solution: Solution, server: Server):
    if len(set(solution.pools)) < 2:
        return solution  # No other pool exists
    no_pools = len(set(solution.pools))
    old_pool_no = solution.pools[server.id]
    new_pool_no = old_pool_no
    while new_pool_no == old_pool_no:
        new_pool_no = random.randint(0, len(set(solution.pools)) - 1)
    solution.pools[server.id] = new_pool_no
    if len(set(solution.pools)) < no_pools:
        return solution  # One pool left unassigned
    return solution


def unassign_server(solution: Solution, server: Server):
    for row_no, row in enumerate(solution.dataCenter):
        for slot_no, slot in enumerate(row):
            if slot == server.id:
                solution.dataCenter[row_no][slot_no:slot_no + server.slots] = [-1] * server.slots
                break  # Stop searching inside row
        else:
            continue  # Next row
        break  # Stop searching rows
    else:
        return solution  # Not found
    return solution


def assign_server_to_first_available_slot(solution: Solution, server: Server):
    for row_no, row in enumerate(solution.dataCenter):
        for slot_no in range(len(row)):
            if row[slot_no:slot_no + server.slots] == [-1] * server.slots:
                solution.dataCenter[row_no][slot_no:slot_no + server.slots] = [server.id] * server.slots
                break  # Stop searching inside row
        else:
            continue  # Next row
        break  # Stop searching rows
    else:
        return solution  # Not found
    return solution

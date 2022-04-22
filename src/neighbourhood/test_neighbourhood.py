from unittest import TestCase

from data_center import Server, Solution

from neighbourhood import assign_server_to_first_available_slot, unassign_server, move_server_inside_row, \
    move_server_to_different_pool, move_server_to_different_row


class TestAssignServerToFirstAvailableSlot(TestCase):
    def test_assign_server_to_first_available_slot_1_row(self):
        server1 = Server(id=0, slots=2, capacity=1)
        solution = Solution(dataCenter=[[-1, -1, -1]], pools=[0])
        solution = assign_server_to_first_available_slot(solution, server1)
        assert solution.dataCenter == [[0, 0, -1]]

    def test_assign_server_to_first_available_slot_2_rows(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [-1, -2, -1],
            [-1, -1, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = assign_server_to_first_available_slot(solution, server1)
        assert solution.dataCenter == [
            [-1, -2, -1],
            [0, 0, -1]
        ]

    def test_assign_server_impossible(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [-1, -2, -1],
            [-1, -2, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = assign_server_to_first_available_slot(solution, server1)
        assert solution is None


class TestUnassignServer(TestCase):
    def test_unassign_server(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [[0, 0, -1]]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = unassign_server(solution, server1)
        assert solution.dataCenter == [[-1, -1, -1]]

    def test_unassign_server_2_rows(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [-2, -2, -1],
            [0, 0, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = unassign_server(solution, server1)
        assert solution.dataCenter == [
            [-2, -2, -1],
            [-1, -1, -1]
        ]

    def test_unassign_server_impossible(self):
        server1 = Server(id=1, slots=2, capacity=1)
        dataCenter = [
            [-2, -2, -1],
            [0, 0, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = unassign_server(solution, server1)
        assert solution is None

    def test_unassign_after_assign(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [-2, -2, -1],
            [-1, -1, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = assign_server_to_first_available_slot(solution, server1)
        assert solution.dataCenter == [
            [-2, -2, -1],
            [0, 0, -1]
        ]
        solution = unassign_server(solution, server1)
        assert solution.dataCenter == [
            [-2, -2, -1],
            [-1, -1, -1]
        ]


class TestMoveServerToDifferentPool(TestCase):
    def test_move_server_to_different_pool_2_pools(self):
        server1 = Server(id=0, slots=2, capacity=1)
        solution = Solution(dataCenter=[], pools=[0, 1, 0])
        solution = move_server_to_different_pool(solution, server1)
        assert solution.pools == [1, 1, 0]

    def test_move_server_to_different_pool_3_pools(self):
        server1 = Server(id=0, slots=2, capacity=1)
        solution = Solution(dataCenter=[], pools=[0, 1, 0, 2])
        solution = move_server_to_different_pool(solution, server1)
        assert solution.pools == [1, 1, 0, 2] or solution.pools == [2, 1, 0, 2]

    def test_move_server_to_different_pool_impossible_1_pool(self):
        server1 = Server(id=0, slots=2, capacity=1)
        solution = Solution(dataCenter=[], pools=[0])
        solution = move_server_to_different_pool(solution, server1)
        assert solution is None

    def test_move_server_to_different_pool_impossible_unassigned_pool(self):
        server1 = Server(id=0, slots=2, capacity=1)
        solution = Solution(dataCenter=[], pools=[2, 1, 0, 0])
        solution = move_server_to_different_pool(solution, server1)
        assert solution is None


class TestMoveServerToDifferentRow(TestCase):
    def test_move_server_to_different_row_2_rows(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [0, 0, -1],
            [-1, -1, -2]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_to_different_row(solution, server1)
        assert solution.dataCenter == [
            [-1, -1, -1],
            [0, 0, -2]
        ]

    def test_move_server_to_different_row_3_rows(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [0, 0, -1],
            [-1, -1, -2],
            [-2, -1, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_to_different_row(solution, server1)
        assert solution.dataCenter == [
            [-1, -1, -1],
            [0, 0, -2],
            [-2, -1, -1]] or solution.dataCenter == [[-1, -1, -1],
                                                     [-1, -1, -2],
                                                     [-2, 0, 0]]

    def test_move_server_to_different_row_impossible(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [0, 0, -1],
            [-1, -2, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_to_different_row(solution, server1)
        assert solution is None


class TestMoveServerInsideRow(TestCase):
    def test_move_server_inside_row_1_slot(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [[0, 0, -1]]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_inside_row(solution, server1)
        assert solution.dataCenter == [[-1, 0, 0]]

    def test_move_server_inside_row_2_slots(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [[0, 0, -1, -1]]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_inside_row(solution, server1)
        assert solution.dataCenter == [[-1, 0, 0, -1]] or solution.dataCenter == [[-1, -1, 0, 0]]

    def test_move_server_inside_row_1_slot_2_rows(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [-1, -1, -1],
            [0, 0, -1]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_inside_row(solution, server1)
        assert solution.dataCenter == [
            [-1, -1, -1],
            [-1, 0, 0]
        ]

    def test_move_server_inside_row_impossible(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [[0, 0]]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_inside_row(solution, server1)
        assert solution is None

    def test_move_server_inside_row_impossible_2_rows(self):
        server1 = Server(id=0, slots=2, capacity=1)
        dataCenter = [
            [-1, -2],
            [0, 0]
        ]
        solution = Solution(dataCenter=dataCenter, pools=[0])
        solution = move_server_inside_row(solution, server1)
        assert solution is None

# if __name__ == '__main__':
#     tes

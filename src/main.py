import sys

from src.algorithms.genetic import genetic
from src.algorithms.hill_climbing import hill_climbing
from src.algorithms.simulated_annealing import simulated_annealing
from src.io.read import read_data_center, write_solution
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import Solution

if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print("Usage: python main.py <input_file> <options>")
        exit(1)

    input_file = sys.argv[1]
    data_center = read_data_center(input_file)

    algorithm = sys.argv[2]
    neighbour_modes = [Neighbourhood.ADD_SV, Neighbourhood.RMV_SV, Neighbourhood.SWTCH_SV_POOL,
                       Neighbourhood.MOV_SV_SLOT, Neighbourhood.SWTCH_SV_ROW]

    it_list = []
    evaluations = []
    no_iterations = 150
    sol: Solution = None
    idk: int = None

    if algorithm == 'genetic':
        population_size = int(sys.argv[3])
        generations = int(sys.argv[4])
        mutation_chance = float(sys.argv[5])
        replaced_each_generation = int(sys.argv[6])
        sol = genetic(data_center, neighbour_modes, population_size, generations, mutation_chance,
                      replaced_each_generation)
    elif algorithm == 'hillclimbing':
        iterations = int(sys.argv[3])
        sol = hill_climbing(data_center, iterations, neighbour_modes)
    elif algorithm == 'simulatedannealing':
        iterations = int(sys.argv[3])
        initial_temperature = float(sys.argv[4])
        temperature_mode = sys.argv[5]
        sol, idk = simulated_annealing(data_center, iterations, neighbour_modes, initial_temperature, temperature_mode)
    else:
        print("Unknown algorithm")
        exit(1)

    write_solution(sol, "/data/solution.txt")

    # pyplot.plot(it_list, evaluations)
    # pyplot.ylabel('Evaluation')
    # pyplot.xlabel('Iteration')
    # pyplot.xlim(0, no_iterations)
    # pyplot.ylim(0, idk + 2)
    # pyplot.show()
    #
    # for i in range(len(it_list)):
    #     print('%d -> eval: %.2f' % (it_list[i], evaluations[i]))

import sys

from src.algorithms.genetic import genetic
from src.algorithms.hill_climbing import hill_climbing_basic_random, hill_climbing_basic, hill_climbing_steepest_ascent
from src.algorithms.simulated_annealing import simulated_annealing, linear_schedule, non_linear_schedule
from src.io.read import read_data_center, write_solution
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import Solution

if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print("Usage: python main.py <input_file> <options>")
        print("Usage: python main.py <input_file> hillclimbing_basic <iterations>")
        print("Usage: python main.py <input_file> hillclimbing_basic_random <iterations>")
        print("Usage: python main.py <input_file> hillclimbing_steepest_ascent <iterations>")
        print("Usage: python main.py <input_file> genetic <generations> <mutation> <replaced_each_gen>")
        print(
            "Usage: python main.py <input_file> simulatedannealing <iterations> <initial_temperature> <temperature_mode>")
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

    if algorithm == 'genetic' or algorithm == 'gen':
        population_size = int(sys.argv[3])
        generations = int(sys.argv[4])
        mutation_chance = float(sys.argv[5])
        replaced_each_generation = int(sys.argv[6])
        sol = genetic(data_center, population_size, generations, mutation_chance,
                      replaced_each_generation)
    elif algorithm == 'hillclimbing_basic_random' or algorithm == 'hcbr':
        iterations = int(sys.argv[3])
        sol = hill_climbing_basic_random(data_center, iterations)
    elif algorithm == 'hillclimbing_basic' or algorithm == 'hcb':
        iterations = int(sys.argv[3])
        sol = hill_climbing_basic(data_center, iterations)
    elif algorithm == 'hillclimbing_steepestascent' or algorithm == 'hcsa':
        iterations = int(sys.argv[3])
        sol = hill_climbing_steepest_ascent(data_center, iterations)
    elif algorithm == 'simulatedannealing' or algorithm == "sa":
        iterations = int(sys.argv[3])
        initial_temperature = float(sys.argv[4])
        temperature_mode = sys.argv[5]
        if temperature_mode == 'linear':
            sol, idk = simulated_annealing(data_center, iterations, initial_temperature, linear_schedule)
        else:
            sol, idk = simulated_annealing(data_center, iterations, initial_temperature, non_linear_schedule)
    else:
        print("Unknown algorithm")
        exit(1)

    write_solution(sol, "data/solution.txt")

    # pyplot.plot(it_list, evaluations)
    # pyplot.ylabel('Evaluation')
    # pyplot.xlabel('Iteration')
    # pyplot.xlim(0, no_iterations)
    # pyplot.ylim(0, idk + 2)
    # pyplot.show()
    #
    # for i in range(len(it_list)):
    #     print('%d -> eval: %.2f' % (it_list[i], evaluations[i]))

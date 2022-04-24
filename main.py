import sys
from matplotlib import pyplot
from graphs import plot_genetic
from src.solution.evaluation import evaluate_solution
from src.algorithms.genetic import genetic
from src.algorithms.hill_climbing import hill_climbing_basic_random, hill_climbing_basic, hill_climbing_steepest_ascent
from src.algorithms.simulated_annealing import simulated_annealing, linear_schedule, non_linear_schedule
from src.algorithms.tabu import tabu_search
from src.io.read import read_data_center, write_solution
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import Solution
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution

import numpy as np
import time

from multiprocessing import Process as worker, Queue



if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print("Usage: python main.py <input_file> <options>")
        print("Usage: python main.py <input_file> hillclimbing_basic <iterations>")
        print("Usage: python main.py <input_file> hillclimbing_basic_random <iterations>")
        print("Usage: python main.py <input_file> hillclimbing_steepest_ascent <iterations>")
        print("Usage: python main.py <input_file> genetic <population_size> <generations> <mutation> <replaced_each_gen>")
        print("Usage: python main.py <input_file> simulatedannealing <iterations> <initial_temperature> <temperature_mode>")
        print("Usage: python main.py <input_file> all <iterations>")
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

    iterations = int(sys.argv[3])
    initial_solution = random_solution(data_center)

    if algorithm == 'genetic' or algorithm == 'gen':
        population_size = int(sys.argv[3])
        generations = int(sys.argv[4])
        mutation_chance = float(sys.argv[5])
        replaced_each_generation = float(sys.argv[6])
        print(population_size)
        sol,_ = genetic(data_center, initial_solution, neighbour_modes,generations, population_size, mutation_chance,
                      replaced_each_generation)

    elif algorithm == 'hillclimbing_basic_random' or algorithm == 'hcbr':
        sol,_ = hill_climbing_basic_random(data_center, iterations, initial_solution)

    elif algorithm == 'hillclimbing_basic' or algorithm == 'hcb':
        sol,_ = hill_climbing_basic(data_center, iterations, initial_solution)

    elif algorithm == 'hillclimbing_steepestascent' or algorithm == 'hcsa':
        sol,_ = hill_climbing_steepest_ascent(data_center, iterations, initial_solution)

    elif algorithm == 'simulatedannealing' or algorithm == "sa":
        initial_temperature = float(sys.argv[4])
        temperature_mode = sys.argv[5]
        if temperature_mode == 'linear':
            sol, _ = simulated_annealing(data_center, iterations, initial_temperature, linear_schedule)
        else:
            sol, _ = simulated_annealing(data_center, iterations, initial_temperature, non_linear_schedule)
    elif algorithm == 'tabu':
        iterations = int(sys.argv[3])
        max_tenure = int(sys.argv[4])
        sol = tabu_search(data_center, iterations, neighbour_modes, max_tenure)
        print(sol)
        print(evaluate_solution(sol, data_center))
    elif algorithm == 'all':

        sol_HC, y_axis_HC = hill_climbing_basic(data_center, iterations, initial_solution)
        sol_GA, y_axis_GA = genetic(data_center, initial_solution, neighbour_modes, iterations, 100, 1,1)
        sol_SA, y_axis_SA = simulated_annealing(data_center, iterations, 100, linear_schedule)
        x_axis = list(range(1, iterations))
    
        pyplot.plot(x_axis, y_axis_HC, color = 'red')
        pyplot.plot(x_axis, y_axis_SA)
        pyplot.plot(x_axis, y_axis_GA, color = 'green')
        pyplot.legend(['Hill Climbing','Simulated Annealing', 'Genetic'])
        pyplot.ylabel('Evaluation')
        pyplot.xlabel('Iteration')
        pyplot.savefig('plots/all.png')
        pyplot.show()
        pyplot.clf()
        exit()
    elif algorithm == 'plotgenetic':
        plot_genetic(data_center,iterations,neighbour_modes)
        exit()

    else:
        print("Unknown algorithm")
        exit()

    print(sol, "->", evaluate_solution(sol,data_center))
    write_solution(sol, "data/solution.txt")




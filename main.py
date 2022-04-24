import sys
from matplotlib import pyplot
from src.solution.evaluation import evaluate_solution
from src.algorithms.genetic import genetic
from src.algorithms.hill_climbing import hill_climbing
from src.algorithms.simulated_annealing import simulated_annealing
from src.io.read import read_data_center, write_solution
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import Solution
from src.solution.solution import random_solution

import numpy as np 
import time
from threading import Thread

ga_values = [[0,0] for x in range(7)]

def timed_genetic(data_center, iterations, neighbour_modes, initial_solution, population_size, mutation_chance, replaced_each_generation, i):
    print("Starting Genetic nº", i)
    sol_GA = [0,0]
    start_time = time.time()
    temp_GA, _ = genetic(data_center, iterations, neighbour_modes, initial_solution, population_size, mutation_chance, replaced_each_generation)
    sol_GA[0] += evaluate_solution(temp_GA,data_center)
    sol_GA[1] += time.time()-start_time
    ga_values[i] = sol_GA
    print("Finished Genetic", i)

def plot_genetic(data_center, iterations, neighbour_modes):
    runs = 1
    initial_solution = random_solution(data_center)

    sol_HC = [0,0]
    start_time = time.time()
    temp_HC, _ = hill_climbing(data_center, iterations, neighbour_modes, initial_solution)
    sol_HC[0] = evaluate_solution(temp_HC,data_center)
    sol_HC[1] = time.time()-start_time
    ga_values[0] = sol_HC

    population_size = 80
    threads = []

    iterations = iterations

    process = Thread(target=timed_genetic, args=[data_center, iterations,neighbour_modes, initial_solution, population_size, 1, 1,1])
    process.start()
    threads.append(process)

    process = Thread(target=timed_genetic, args=[data_center, iterations,neighbour_modes, initial_solution, population_size, 0.1, 1,2])
    process.start()
    threads.append(process)

    process = Thread(target=timed_genetic, args=[data_center, iterations,neighbour_modes, initial_solution, population_size, 0.01, 1,3])
    process.start()
    threads.append(process)

    process = Thread(target=timed_genetic, args=[data_center, iterations,neighbour_modes, initial_solution, population_size, 1, 0.5,4])
    process.start()
    threads.append(process)

    process = Thread(target=timed_genetic, args=[data_center, iterations,neighbour_modes, initial_solution, population_size, 0.1, 0.5,5])
    process.start()
    threads.append(process)

    process = Thread(target=timed_genetic, args=[data_center, iterations,neighbour_modes, initial_solution, population_size, 0.01, 0.5,6])
    process.start()
    threads.append(process)

    # We now pause execution on the main thread by 'joining' all of our started threads.
    # This ensures that each has finished processing the urls.
    for process in threads:
        process.join()

    print(ga_values)
    evaluations = [v[0]/runs for v in ga_values]
    times = [v[1]/runs for v in ga_values]
    algorithms = ["Hill\nClimbing", 
    "100% MUT\n100% REG",
    '10% MUT\n100% REG',
    '1% MUT\n100% REG',    
    "100% MUT\n50% REG",
    '10% MUT\n50% REG',
    '1% MUT\n50% REG']

    x_axis = np.arange(len(algorithms))
    pyplot.figure(figsize=(8, 5))
    pyplot.bar(x_axis - 0.2, evaluations,width=0.4,color='red', label='value')
    pyplot.bar(x_axis + 0.2, times,width=0.4, color = 'pink', label='time')
    pyplot.legend()
    pyplot.xticks(x_axis, algorithms)
    pyplot.title('Genetic Algorithm')
    pyplot.savefig('plots/genetic.png')
    pyplot.show()


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print("Usage: python main.py <input_file> <options>")
        print("Usage: python main.py <input_file> hillclimbing <iterations>")
        print("Usage: python main.py <input_file> genetic <generations> <mutation> <replaced_each_gen>")
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
        replaced_each_generation = int(sys.argv[6])
        sol = genetic(data_center, neighbour_modes, population_size, generations, mutation_chance,
                      replaced_each_generation)
    elif algorithm == 'hillclimbing' or algorithm == 'hc':
        iterations = int(sys.argv[3])
        sol_HC, y_axis_HC = hill_climbing(data_center, iterations, neighbour_modes)
    elif algorithm == 'simulatedannealing' or algorithm == "sa":
        iterations = int(sys.argv[3])
        initial_temperature = float(sys.argv[4])
        temperature_mode = sys.argv[5]
        sol_SA, y_axis_SA = simulated_annealing(data_center, iterations, neighbour_modes, initial_temperature, temperature_mode)
    elif algorithm == 'all':

        sol_HC, y_axis_HC = hill_climbing(data_center, iterations, neighbour_modes, initial_solution)
        sol_GA, y_axis_GA = genetic(data_center, iterations, neighbour_modes, initial_solution, 100, 1,1)
        sol_SA, y_axis_SA = simulated_annealing(data_center, iterations, neighbour_modes, 100, 'linear', initial_solution)
        x_axis = list(range(1, iterations))
        
        pyplot.plot(x_axis, y_axis_HC, color = 'red')
        pyplot.plot(x_axis, y_axis_SA)
        pyplot.plot(x_axis, y_axis_GA, color = 'green')
        pyplot.legend(['Hill Climbing','Simulated Annealing', 'Genetic'])
        pyplot.ylabel('Evaluation')
        pyplot.xlabel('Iteration')
        pyplot.savefig('plots/all.png')
        pyplot.clf()
        exit()
    elif algorithm == 'plotgenetic':
        plot_genetic(data_center,iterations,neighbour_modes)
        exit()
    else:
        print("Unknown algorithm")
        exit()

    write_solution(sol, "data/solution.txt")




import sys
from matplotlib import pyplot
from src.algorithms.hill_climbing import hill_climbing_basic
from src.solution.evaluation import evaluate_solution
from src.algorithms.genetic import genetic
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import Solution
from src.solution.solution import random_solution

import numpy as np 
import time

from multiprocessing import Process as worker, Queue


def timed_genetic(data_center, iterations, neighbour_modes, initial_solution, population_size, mutation_chance, replaced_each_generation, i, res):
    print("Starting Genetic nº", i)
    sol_GA = [0,0]
    start_time = time.time()
    temp_GA, _ = genetic(data_center, initial_solution, neighbour_modes, iterations, population_size, mutation_chance, replaced_each_generation)
    sol_GA[0] += evaluate_solution(temp_GA,data_center)
    sol_GA[1] += time.time()-start_time
    print("Finished Genetic nº", i)
    res.put([sol_GA, i])

def plot_genetic(data_center, iterations, neighbour_modes):
    runs = 1
    initial_solution = random_solution(data_center)
    ga_values = [[0,0] for x in range(7)]

    sol_HC = [0,0]
    start_time = time.time()
    temp_HC, _ = hill_climbing_basic(data_center, iterations, initial_solution)
    sol_HC[0] = evaluate_solution(temp_HC,data_center)
    sol_HC[1] = time.time()-start_time
    ga_values[0] = sol_HC

    population_size = 80
    threads = []

    iterations = iterations

    res = Queue()

    process = worker(target=timed_genetic, args=(data_center, iterations,neighbour_modes, initial_solution, population_size, 1, 1,1,res))
    process.start()
    threads.append(process)

    process = worker(target=timed_genetic, args=(data_center, iterations,neighbour_modes, initial_solution, population_size, 0.1, 1,2,res))
    process.start()
    threads.append(process)

    process = worker(target=timed_genetic, args=(data_center, iterations,neighbour_modes, initial_solution, population_size, 0.01, 1,3,res))
    process.start()
    threads.append(process)

    process = worker(target=timed_genetic, args=(data_center, iterations,neighbour_modes, initial_solution, population_size, 1, 0.5,4,res))
    process.start()
    threads.append(process)

    process = worker(target=timed_genetic, args=(data_center, iterations,neighbour_modes, initial_solution, population_size, 0.1, 0.5,5,res))
    process.start()
    threads.append(process)

    process = worker(target=timed_genetic, args=(data_center, iterations,neighbour_modes, initial_solution, population_size, 0.01, 0.5,6,res))
    process.start()
    threads.append(process)

    # We now pause execution on the main thread by 'joining' all of our started threads.
    # This ensures that each has finished processing the urls.
    for process in threads:
        sol, i = res.get()
        ga_values[i] = sol
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




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

RUNS = 1


def timed_genetic(data_center, iterations, neighbour_modes, initial_solution, population_size, mutation_chance, replaced_each_generation, i, res):
    print("Starting Genetic nº", i)
    sol_GA = [0,0]
    for run in range(RUNS):
        start_time = time.time()
        temp_GA, y_axis_GA = genetic(data_center, initial_solution, neighbour_modes, iterations, population_size, mutation_chance, replaced_each_generation)
        sol_GA[0] += evaluate_solution(temp_GA,data_center)
        sol_GA[1] += time.time()-start_time
    print("Finished Genetic nº", i)
    res.put([sol_GA,y_axis_GA, i])

def timed_hill_climbing(data_center,iterations, initial_solution,i,res):
    print("Starting Hill Climbing")
    sol_HC = [0,0]

    for run in range(RUNS):
        start_time = time.time()
        temp_HC, y_axis_HC = hill_climbing_basic(data_center, iterations, initial_solution)
        sol_HC[0] = evaluate_solution(temp_HC,data_center)
        sol_HC[1] = time.time()-start_time
    print("Finished Hill Climbing")
    res.put([sol_HC,y_axis_HC,i])


def plot_genetic(data_center, iterations, neighbour_modes):
    initial_solution = random_solution(data_center)
    ga_values = [[0,0] for x in range(7)]

    population_size = 80
    threads = []

    res = Queue()

    process = worker(target=timed_hill_climbing, args=(data_center, iterations, initial_solution,0,res))
    process.start()
    threads.append(process)

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
        sol, y_axis, i = res.get()
        ga_values[i] = sol[0], sol[1],y_axis
        process.join()

    evaluations = [v[0]/RUNS for v in ga_values]
    times = [v[1]/RUNS for v in ga_values]
    time_label = "time (sec)"
    if(max(times) > max(evaluations)):
        times = [t/10 for t in times]
        time_label = "time (decasec)"
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
    pyplot.bar(x_axis + 0.2, times,width=0.4, color = 'pink', label=time_label)
    pyplot.legend(loc=(1.05,0.5))
    pyplot.xticks(x_axis, algorithms)
    pyplot.title('Genetic Algorithm')
    pyplot.savefig('plots/genetic_bar.png',bbox_inches='tight')
    pyplot.clf()

    x_axis = list(range(1, iterations))
    colors = ['blue', 'cyan', 'green', 'yellow', 'orange','red','purple']
    for i, v in enumerate(ga_values):
        pyplot.plot(x_axis, v[2], color = colors[i])

    pyplot.legend(algorithms,loc=(1.05,0.5))
    pyplot.ylabel('Evaluation')
    pyplot.xlabel('Iteration')
    pyplot.savefig('plots/genetic_line.png',bbox_inches='tight')




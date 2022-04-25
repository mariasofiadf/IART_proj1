from dataclasses import dataclass
import sys
from markupsafe import string
from matplotlib import pyplot
from src.algorithms.simulated_annealing import linear_schedule, simulated_annealing
from src.algorithms.tabu import tabu_search
from src.algorithms.hill_climbing import hill_climbing_basic
from src.solution.evaluation import evaluate_solution
from src.algorithms.genetic import genetic
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import DataCenter, Solution
from src.solution.solution import random_solution

import numpy as np 
import time

from multiprocessing import Process as worker, Queue
from operator import add
RUNS = 1

@dataclass
class Args:
    data_center: DataCenter
    iterations: int 
    initial_solution: Solution
    q: Queue
    i: int 
    population_size: int
    mutation_chance: int
    replaced_each_generation: int
    func: string
    neighbour_modes: list()

def timed_func(args: Args):
    sol = [0,0]
    y_axis = [0 for i in range(args.iterations-1)]

    print(args.i, "Starting ", args.func)
    for run in range(RUNS):
        start_time = time.time()

        if(args.func == 'genetic'):
            temp, y_axis_temp = genetic(args.data_center, args.initial_solution, args.neighbour_modes, args.iterations, args.population_size, args.mutation_chance, args.replaced_each_generation)
        elif(args.func == 'hillclimb'):
            temp, y_axis_temp = hill_climbing_basic(args.data_center, args.iterations, args.initial_solution)
        elif(args.func == 'tabu'):
            temp, y_axis_temp = tabu_search(args.data_center, args.iterations, args.neighbour_modes, args.max_tenure)
        elif(args.func == 'annealing'):
            temp, y_axis_temp = simulated_annealing(args.data_center, args.iterations, args.init_temp, args.schedule_func)
        else:
            print("Error: Invalid algorithm")
            exit()
        
        y_axis = list( map(add, y_axis, y_axis_temp) )
        sol[0] += evaluate_solution(temp,args.data_center)
        sol[1] += time.time()-start_time

    print(args.i, "Finished ", args.func)

    y_axis_GA = [y/RUNS for y in y_axis] # Calculate average y at each iteration
    sol = (sol[0]/RUNS, sol[1]/RUNS) # Calculate averages of time and value

    args.q.put([sol,y_axis_GA, args.i])


def plot_genetic(data_center, iterations, neighbour_modes):
    initial_solution = random_solution(data_center)
    ga_values = [[0,0] for x in range(7)]

    population_size = 80
    threads = []

    q = Queue()

    args = Args(data_center, iterations, initial_solution,q,0,population_size,1,1, 'hillclimb', neighbour_modes)

    process = worker(target=timed_func, args=(args,))
    process.start()
    threads.append(process)

    args.i, args.func = 1,'genetic'
    process = worker(target=timed_func, args = (args,))
    process.start()
    threads.append(process)

    args.mutation_chance, args.i = 0.1, 2
    process = worker(target=timed_func, args = (args,))
    process.start()
    threads.append(process)

    args.mutation_chance, args.i = 0.01, 3
    process = worker(target=timed_func, args=(args,))
    process.start()
    threads.append(process)

    args.mutation_chance, args.replaced_each_generation, args.i = 1, 0.5, 4
    process = worker(target=timed_func, args = (args,))
    process.start()
    threads.append(process)

    args.mutation_chance, args.i = 0.1, 5
    process = worker(target=timed_func, args=(args,))
    process.start()
    threads.append(process)

    args.mutation_chance, args.i = 0.01, 6
    process = worker(target=timed_func, args =(args,))
    process.start()
    threads.append(process)

    # We now pause execution on the main thread by 'joining' all of our started threads.
    # This ensuq that each has finished processing the urls.
    for process in threads:
        sol, y_axis, i = q.get()
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
    ax = pyplot.gca()
    pyplot.savefig('plots/genetic_bar.png',bbox_inches='tight')
    pyplot.clf()

    x_axis = list(range(1, iterations))
    colors = ['blue', 'cyan', 'green', 'yellow', 'orange','red','purple']
    for i, v in enumerate(ga_values):
        pyplot.plot(x_axis, v[2], color = colors[i])
    pyplot.legend(algorithms,loc=(1.05,0.2))
    pyplot.ylabel('Evaluation')
    pyplot.xlabel('Iteration')
    ax = pyplot.gca()
    pyplot.savefig('plots/genetic_line.png',bbox_inches='tight')




def plot_all(data_center, iterations, initial_solution, neighbour_modes):
    return

#     q = Queue()
#     threads = []
#     values = [[0,0] for x in range(4)]
#     print(iterations)

#     process = worker(target=timed_hill_climbing, args'[(']data_center, iterations, initial_solution,0,q))
#     process.start()
#     threads.append(process)
    
#     process = worker(target=timed_func, args'[(']data_center, iterations,neighbour_modes, initial_solution, 80, 1, 1,1,q))
#     process.start()
#     threads.append(process)

#     process = worker(target=timed_annealing, args'[(']data_center, iterations,100, linear_schedule,2,q))
#     process.start()
#     threads.append(process)

#     process = worker(target=timed_tabu, args'[(']data_center, iterations,neighbour_modes, initial_solution, 10,3,q))
#     process.start()
#     threads.append(process)

#     for process in threads:
#         sol, y_axis, i = q.get()
#         values[i] = sol[0], sol[1],y_axis
#         process.join()


#     evaluations = [v[0]/RUNS for v in values]
#     times = [v[1]/RUNS for v in values]
#     time_label = "time (sec)"
#     if(max(times) > max(evaluations)):
#         times = [t/10 for t in times]
#         time_label = "time (decasec)"
    
#     algorithms = ["Hill\nClimbing",  'Genetic', 'Simulated Annealing','Tabu Search']


#     ## Plot bar graph 
#     x_axis = np.arange(len(algorithms))
#     print(x_axis)
#     print(evaluations)
#     print(times)
#     pyplot.figure(figsize=(8, 5))
#     pyplot.bar(x_axis - 0.2, evaluations,width=0.4,color='red', label='value')
#     pyplot.bar(x_axis + 0.2, times,width=0.4, color = 'pink', label=time_label)
#     pyplot.legend(loc=(1.05,0.5))
#     pyplot.xticks(x_axis, algorithms)
#     pyplot.title('Algorithms Comparison')
#     ax = pyplot.gca()
#     pyplot.savefig('plots/all_bar.png',bbox_inches='tight')
#     pyplot.clf()

#     ## Plot line graph
#     x_axis = list(range(1, iterations))
#     colors = ['blue', 'cyan', 'green', 'yellow', 'orange','red','purple']
#     x_shape = 0
#     for i, v in enumerate(values):
#         ys = v[2]
#         x_shape = max(x_shape, len(ys))
#         while(len(ys)<x_shape):
#             ys.append(ys[-1])
#         pyplot.plot(x_axis, ys, color = colors[i])

#     pyplot.legend(algorithms,loc=(1.05,0.2))
#     pyplot.ylabel('Evaluation')
#     pyplot.xlabel('Iteration')
#     ax = pyplot.gca()
#     pyplot.savefig('plots/all_line.png',bbox_inches='tight')

from random import random, choices
from src.solution.data_center import DataCenter, Solution
from src.solution.evaluation import evaluate_solution
from src.neighbourhood.neighbourhood import assign_server_to_first_available_slot, neighbourhood
from src.solution.solution import randomSolution
import sys

def geneticAlgorithm(config: DataCenter, neighbourModes, populationSize = 100, generations = 1000, mutationChance = 0.1, replacedEachGeneration = 100):
    # Get first generation
    population = []
    for i in range(populationSize):
        solution = randomSolution(config)
        population.append(solution)

    bestSolution = population[0]

    # Generate generations
    for gen in range(generations):
        population = getOffspring(population, config, mutationChance,neighbourModes)

        # Get best solution of current population
        for sol in population:
            if(evaluate_solution(sol, config) > evaluate_solution(bestSolution, config)):
                bestSolution = sol
        

    return bestSolution


def getOffspring(population, config, mutationChance, neighbourModes):
    populationValues = [evaluate_solution(sol,config) for sol in population]
    summ = sum(populationValues)+ sys.float_info.min # sum of evaluation of solutions

    # Get roulette values for population
    roulette = [val/summ for val in populationValues]
    if(roulette.count(0) > len(roulette)-2):
        roulette = [summ/len(roulette) for r in roulette]
        
    newPopulation = []

    popSize = len(population)

    # While the population is not complete, get parents (using roulette method) and reproduce
    while(len(newPopulation) < popSize):
        #Get parent 1 according to roulette
        x = (choices(population, roulette))[0]

        while True:
            #Get parent 2 that is different to parent 1
            y = (choices(population, roulette))[0]
            if( y != x or len(set(roulette))==1):
                break

        # Reproduce
        child = reproduce(x,y,config)
        r = random()

        # Mutate if necessary
        if(r < mutationChance):
            child = neighbourhood(child,neighbourModes,config)

        # Add child to population
        newPopulation.append(child)

    return newPopulation

def reproduce(x: Solution, y: Solution, config: DataCenter):
    poolLength = len(x.pools)

    #Mix pools of parent 1 with pools of parent 2 Fix point crossover
    pools = x.pools[0:poolLength//2] + y.pools[poolLength//2::]

    dataCenter =[[-1 for r in range(len(x.dataCenter[0]))] for s in range(len(x.dataCenter))]

    for r, row in enumerate(x.dataCenter):
        for s, slot in enumerate(row):
            if( slot == -2):
                dataCenter[r][s] = slot

    # Get half of parent 1's rows and assign to child
    for r, row in enumerate(x.dataCenter):
        for s, slot in enumerate(row[:len(row)//2]):
            dataCenter[r][s] = slot
            i = 1
            while(x.dataCenter[r][s] == x.dataCenter[r][s+i]):
                dataCenter[r][s+i] = x.dataCenter[r][s+i]
                i+=1
                if(s+i > len(dataCenter[0])-1):
                    break

    child = Solution(pools, dataCenter)

    # Fill the rest of the slots with information from parent 2
    for r in y.dataCenter:
        for s in r:
            if(not any(s in row for row in dataCenter) and s >= 0):
                assign_server_to_first_available_slot(child,config.getServer(s))

    return child



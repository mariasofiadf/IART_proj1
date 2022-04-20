
from random import random, choices
from django.urls import conf
from dataCenter import DataCenter, Solution
from evaluation import evaluate_solution
from neighbourhood import assign_server_to_first_available_slot, neighbourhood
from solution import randomSolution
import sys

def geneticAlgorithm(config: DataCenter, neighbourModes, populationSize = 100, generations = 100, mutationChance = 1, replacedEachGeneration = 100):
    # Get first generation
    population = []
    for i in range(populationSize):
        solution = randomSolution(config)
        population.append(solution)

    bestSolution = population[0]

    for gen in range(generations):
        print("Generation: ", gen)
        population = getOffspring(population, config, mutationChance,neighbourModes)
        # Get best solution
        for sol in population:
            if(evaluate_solution(sol, config) > evaluate_solution(bestSolution, config)):
                bestSolution = sol
        

    return bestSolution


def getOffspring(population, config, mutationChance,neighbourModes):
    populationValues = [evaluate_solution(sol,config) for sol in population]
    summ = sum(populationValues)+ sys.float_info.min # sum of evaluation of solutions
    roulette = [val/summ for val in populationValues]
    if(roulette.count(0) > len(roulette)-2):
        roulette = [summ/len(roulette) for r in roulette]
    newPopulation = []

    popSize = len(population)
    while(len(newPopulation) < popSize):
        x = (choices(population, roulette))[0]
        while True:
            y = (choices(population, roulette))[0]
            if( y != x or len(set(roulette))==1):
                break
        child = reproduce(x,y,config)
        r = random()
        if(r < mutationChance):
            child = neighbourhood(child,neighbourModes,config)
        newPopulation.append(child)


    return newPopulation

def reproduce(x: Solution, y: Solution, config: DataCenter):
    poolLength = len(x.pools)
    pools = x.pools[0:poolLength//2] + y.pools[poolLength//2::]

    dataCenter =[[-1 for r in range(len(x.dataCenter[0]))] for s in range(len(x.dataCenter))]

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

    for r in y.dataCenter:
        for s in r:
            if(not any(s in row for row in dataCenter) and s >= 0):
                assign_server_to_first_available_slot(child,config.getServer(s))

    return child



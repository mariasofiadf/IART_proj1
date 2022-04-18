
from django.urls import conf
from dataCenter import DataCenter
from evaluation import evaluate
from solution import randomSolution

def geneticAlgorithm(config: DataCenter, populationSize = 100, generations = 100, mutationChance = 1, replacedEachGeneration = 100):
    # Get first generation
    population = []
    for i in range(populationSize):
        solution = randomSolution(config)
        population.append(solution)

    # Get best solution
    bestSolution = population[0]
    for sol in population:
        if(evaluate(sol, config) > evaluate(bestSolution, config)):
            bestSolution = sol

    return bestSolution




from dataCenter import DataCenter, Solution
from evaluation import evaluate
from neighbourhood import neighbourhood
from solution import randomSolution


def hillClimbing(config: DataCenter, iterations: int, neighbourModes):
    solution = randomSolution(config)
    for i in range(iterations):
        newSolution = neighbourhood(solution,neighbourModes,config)
        print(newSolution)
        if(evaluate(newSolution, config) >= evaluate(solution,config)):
            print('>%d f(%s) => %.5f' % (i, newSolution, evaluate(solution,config)))
            solution = newSolution
    return solution
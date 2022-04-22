from data_center import DataCenter, Solution
from evaluation import evaluate_solution  
from neighbourhood import neighbourhood
from solution import randomSolution


def hillClimbing(config: DataCenter, iterations: int, neighbourModes):
    solution = randomSolution(config)
    for i in range(iterations):
        newSolution = neighbourhood(solution,neighbourModes,config)
        print(newSolution)
        if(evaluate_solution(newSolution, config) >= evaluate_solution(solution,config)):
            print('>%d f(%s) => %.5f' % (i, newSolution, evaluate_solution(solution,config)))
            solution = newSolution
    return solution
from src.neighbourhood.neighbourhood import neighbourhood
from src.solution.data_center import DataCenter, Solution
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution


def hill_climbing(config: DataCenter, iterations: int, neighbourModes, solution: Solution):
    evaluations = list()
    for i in range(iterations -1):
        newSolution = neighbourhood(solution,neighbourModes,config)
        newSolution_eval = evaluate_solution(newSolution, config)
        currSolution_eval = evaluate_solution(solution,config)
        if(newSolution_eval >=  currSolution_eval):
            #print('>%d f(%s) => %.5f' % (i, newSolution, evaluate_solution(solution,config)))
            solution = newSolution
        evaluations.append(currSolution_eval)
    return [solution, evaluations]
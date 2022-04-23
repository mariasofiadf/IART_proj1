from dataCenter import DataCenter, Solution
from evaluation import evaluate_solution  
from neighbourhood import neighbourhood

def hillClimbing(config: DataCenter, iterations: int, neighbourModes, solution: Solution):
    evaluations = list()
    for i in range(iterations -1):
        newSolution = neighbourhood(solution,neighbourModes,config)
        newSolution_eval = evaluate_solution(newSolution, config)
        evaluations.append(newSolution_eval)
        print(newSolution)
        if(newSolution_eval >= evaluate_solution(solution,config)):
            print('>%d f(%s) => %.5f' % (i, newSolution, evaluate_solution(solution,config)))
            solution = newSolution
    return [solution, evaluations]
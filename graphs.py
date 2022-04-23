from matplotlib import pyplot
from solution import randomSolution
from read import readDataCenter
from neighbourhood import Neighbourhood
from hillClimbing import hillClimbing
from simAnnealing import simulatedAnnealing


config = readDataCenter('problem.txt')
initial_solution = randomSolution(config)
neighbourModes = [Neighbourhood.ADD_SV,Neighbourhood.RMV_SV,Neighbourhood.SWTCH_SV_POOL, Neighbourhood.MOV_SV_SLOT, Neighbourhood.SWTCH_SV_ROW, Neighbourhood.SWTCH_SV_POOL]
iter = 100
x_axis = list(range(1, iter))

temp = 150


sol_AS, y_axis_AS  = simulatedAnnealing(config, iter, neighbourModes, temp, 'linear', initial_solution)


sol_HC, y_axis_HC = hillClimbing(config, iter, neighbourModes,initial_solution)

pyplot.plot(x_axis, y_axis_AS)
pyplot.plot(x_axis, y_axis_HC, color = 'red')
pyplot.ylabel('Evaluation')
pyplot.xlabel('Iteration')
pyplot.show()



import numpy as np
import math

def fitness_function(name):
	#decent
	if name == "Rastrigin":
		def rastringin(x):
			n = len(x)
			A = 10
			return A * n + np.sum([(xi ** 2 - A * np.cos(2 * math.pi * xi)) for xi in x])
		
		return rastringin
	#terribleo
	elif name == "Schwefel":

		def schwefelFunction(xArr):
			n = len(xArr)
			return n * 418.9829 + np.sum([x * np.sin(np.sqrt(np.abs(x))) for x in xArr])
		
		return schwefelFunction

	#??? wut xD
	elif name == "Rosenbrock":

		def rosenbrockFunction(xArr):
			x = xArr[0]
			y = xArr[1]
			return 100 * np.square((np.square(x) - y)) + np.square((1-x))

		return rosenbrockFunction
	#good
	elif name == "Griewangk":

		def griewangkFunction(x):
			partA = 0
			partB = 1
			for i in range(np.shape(x)[0]):
				partA += x[i]**2
				partB *= np.cos(float(x[i]) / np.sqrt(i+1))
			return 1 + (float(partA)/4000.0) - float(partB)
		  
		return griewangkFunction
	#good
	elif name == "Ackley":

		def ackleyFunction(xArr):
			n = len(xArr)
			return  20 + np.e - 20.0 * np.exp(-0.2 * np.sqrt(1/n * sum([np.square(x) for x in xArr])))-np.exp(1/n * sum([np.cos(2 * np.pi * x) for x in xArr]))  
		
		return ackleyFunction


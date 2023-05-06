import math
import numpy as np
import math
import random
from individuals import Individual
import copy
import time

#Responsible for evolving the population


def vectorTwoPointCrossover(individual1, individual2, probability, ind_deviation, function_name):

	cut1 = random.randint(1, len(individual1)/2)
	cut2 = random.randint(cut1+1, len(individual1))

	for i in range(3):
		if(random.random() < probability):
			if(i == 0):
				individual1, individual2 = individual2[0:cut1] + individual1[cut1:], individual1[0:cut1] + individual2[cut1:]
			elif(i == 1):
				individual1, individual2 =  individual1[0:cut1] + individual2[cut1:cut2] + individual1[cut2:],  individual2[0:cut1] + individual1[cut1:cut2] + individual2[cut2:]
			else:
				individual1, individual2  = individual1[:cut2] + individual2[cut2:], individual2[:cut2] + individual1[cut2:]
	
	return Individual(individual1, ind_deviation, function_name), Individual(individual2, ind_deviation, function_name)
	

# Tournament Selection of size 5. Randomly selects 5 individuals from the population and return the 2 with the best fitness. 
# population -> array containing the individuals that have a chance to be selected
# Adapted from https://stackoverflow.com/questions/59446918/genetic-algorithm-tournament-selection-random-choice-pick-same-parents
def tournamentSelection(population):
	parents = random.choices(population, k=5)
	parents = sorted(parents, key=lambda agent: agent.fitness, reverse=False)
	return parents[0], parents[1]



def elitism(amount_elitism, old_population, new_population):
		size = len(old_population)
		sorted_population = sorted(old_population, key=lambda indiv: indiv.fitness)
		sorted_new_population = sorted(new_population, key=lambda indiv: indiv.fitness)

		return sorted_population[:amount_elitism] + sorted_new_population[:size - amount_elitism]
	
#Evolves a population according to input parameters
#population -> population to evolve
#number_generations -> number of generations that will be used to evolve the population
#mutation_prob -> probability of mutation occuring 
#crossover_prob -> probability of crossover occuring 
def evolution(population, number_generations, mutation_prob, offset_mutation, crossover_prob, elitism_percentage):

	best_arr = []
	average_fit = []
	average_deviation = []

	elitist_individuals = math.floor(len(population) * elitism_percentage)

	start_time = time.time()
	for j in range(number_generations):
		
		#print("G:", j)

		new_population = []

		#Two point Crossover 
		for _ in range(0, (len(population)) //2):
			indiv1, indiv2 = tournamentSelection(population)
			offspring1, offspring2 = vectorTwoPointCrossover(copy.deepcopy(indiv1.value_arr), copy.deepcopy(indiv2.value_arr) , crossover_prob, (indiv1.deviation + indiv2.deviation) / 2, indiv1.function_name)

			new_population.append(offspring1)
			new_population.append(offspring2)

		#Mutation
		for indiv in new_population:
			indiv.mutation(mutation_prob, offset_mutation)
			fitness = indiv.fitness_function(indiv.value_arr)
			
			if fitness < indiv.fitness: 
				indiv.deviation = indiv.new_deviation
			
			indiv.fitness = fitness
			indiv.new_deviation = indiv.deviation

		population = elitism(elitist_individuals, population, new_population)

		# average of each generation    
		average_fit.append(get_average_fitness(population))

		# best of each generation
		best_arr.append(get_best_individual(population).fitness)

		average_deviation.append(get_average_deviation(population))
	
	best_individual = get_best_individual(population)
	print("Run ended! Time: ", time.time() - start_time)
	return best_arr, average_fit, average_deviation, best_individual

#Returns the average value of the deviation of mutation in a population
def get_average_deviation(population):
	sum_deviation = 0 
	for individual in population:
		sum_deviation += individual.deviation
	return sum_deviation / len(population)   

#Returns the fitness of the best individual of a population
def get_best_individual(population):
	best_fitness = math.inf
	for individual in population:
		if individual.fitness <= best_fitness: 
				best_fitness = individual.fitness
				indiv = individual
	return indiv

#Returns the average fitness of a population	
def get_average_fitness(population):
	sum_fitness = 0
	for individual in population:
		sum_fitness += individual.fitness
	return sum_fitness / len(population)

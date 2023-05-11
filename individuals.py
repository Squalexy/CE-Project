#Script with the individual class and the functions to modify the individuals and initiate the populations
import random
import numpy as np
from fitness_functions import fitness_function

class Individual:

   #Constructor of the individual class
   # array_length -> size of the array of an individual (how many numbers each individual has)
   # lb -> function lower bound
   # ub -> function upper bound
   # init -> initial deviation   

    def __init__(self, *index):

        if(len(index) == 5):
            array_length = index[0]
            lb = index[1]
            ub = index[2]
            init_deviation = index[3] 
            function_name = index[4]
            self.value_arr = self.create_individual(array_length, lb, ub) 
            self.deviation = init_deviation
            self.new_deviation = init_deviation
            self.function_name = function_name
            self.lb = lb
            self.ub = ub

            #initialize fitness
            self.fitness_function = fitness_function(function_name)
            self.fitness = self.fitness_function(self.value_arr)

        elif(len(index) == 3):

            self.value_arr = index[0]
            self.deviation = index[1]
            self.function_name = index[2]

            self.new_deviation = self.deviation
            self.fitness_function = fitness_function(self.function_name)
            self.fitness = self.fitness_function(self.value_arr)


    #Creates an individual
    def create_individual(self, array_length, lb, ub):
        individual = []

        for _ in range(array_length):
            individual.append(random.uniform(lb,ub))

        return individual
    
    def mutation(self, probability, offset):
        self.mutate_dev(offset)
    
        for value_indx in range(len(self.value_arr)):
            r = np.random.random()

            if r < probability:
                self.value_arr[value_indx] = random.gauss(self.value_arr[value_indx], self.new_deviation)


    def mutate_dev(self, offset):
        self.new_deviation = random.gauss(self.new_deviation, offset)

        if self.new_deviation < 0:
            self.new_deviation = -self.new_deviation

        # if self.new_deviation < 0:
        #     self.new_deviation = 0
        #print("After: ", self.new_deviation)


#Creates a population of n individuals
def create_population(n_individuals, array_length, lb, ub, init_deviation, function_name):

    return [Individual(array_length, lb, ub, init_deviation, function_name) for _ in range(n_individuals)]
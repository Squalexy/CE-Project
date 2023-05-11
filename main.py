#Main script to run the project.
import os
from individuals import create_population
from evolution import evolution
from plots import plot_all, plot_all_box, save_best_individual, countFiles, makeDir, makeConfigFile, save_best_runs
import numpy as np 
import copy


def run_experiments(n_runs, n_individuals, array_length, lb, ub, init_deviation, function_name, number_generations, mutation_prob, offset_mutation, crossover_prob, elitism_percentage):

    best_of_each_run = []
    average_of_each_run = []
    deviation_of_each_run = []
    global_best_individual = None

    for i in range(n_runs):
        print("Run: ", str(i))
        pop = create_population(n_individuals, array_length, lb, ub, init_deviation, function_name)

        run_best, run_average, run_deviation, best_individual = evolution(pop, number_generations, mutation_prob, offset_mutation, crossover_prob, elitism_percentage)

        if global_best_individual is None or best_individual.fitness < global_best_individual.fitness:
            global_best_individual = best_individual

        
        best_of_each_run.append(copy.deepcopy(run_best))
        average_of_each_run.append(copy.deepcopy(run_average))
        deviation_of_each_run.append(copy.deepcopy(run_deviation))

    return best_of_each_run, average_of_each_run, deviation_of_each_run, global_best_individual


def main():

    n_runs = 30
    lb = -5.12
    ub = 5.12
    n_individuals = 90
    array_length = 40
    init_deviation = 0.5
    number_generations = 20
    mutation_prob = 0.1
    crossover_prob = 0.3
    offset_mutation = 3
    elitism_percentage = 0.1
    function_name = "Griewangk"

    if not os.path.exists("Plots"):
        os.mkdir("Plots")
        
    if not os.path.exists("Plots/experiments"):
        os.mkdir("Plots/experiments")
        
    path = os.getcwd()+"/Plots/experiments/"
  
    makeDir(path, str(function_name) + "_" + str(ub))
    dir_path = path + "/" + str(function_name) + "_" + str(ub)
    makeConfigFile("Config.txt", dir_path, function_name, n_runs, number_generations, array_length, n_individuals, init_deviation, offset_mutation, mutation_prob, crossover_prob)

    # [[indiv,indiv,indiv,...],  [indiv,indiv,indiv,...], ...] -> size 30 of tests, size 200 of each population for example
    best_of_each_run_deviation, average_of_each_run_deviation, deviation_of_each_run, global_best_individual_deviation = run_experiments(n_runs, n_individuals, array_length, lb, ub, init_deviation, function_name, number_generations, mutation_prob, offset_mutation, crossover_prob, elitism_percentage)

    print(np.size(deviation_of_each_run))

    global_best_deviation = [float(min(l)) for l in zip(*best_of_each_run_deviation)]
    best_value_average_deviation = [float(sum(l))/len(l) for l in zip(*best_of_each_run_deviation)]
    average_value_average_deviation = [float(sum(l))/len(l) for l in zip(*average_of_each_run_deviation)]
    deviation_average = [float(sum(l))/len(l) for l in zip(*deviation_of_each_run)]

    print(np.size(deviation_average))

    #---NORMAL OPERATION---
    offset_mutation = 0
    best_of_each_run_normal, average_of_each_run_normal, _ , global_best_individual_normal = run_experiments(n_runs, n_individuals, array_length, lb, ub, init_deviation, function_name, number_generations, mutation_prob, offset_mutation, crossover_prob, elitism_percentage)

    global_best_normal = [float(min(l)) for l in zip(*best_of_each_run_normal)]
    best_value_average_normal = [float(sum(l))/len(l) for l in zip(*best_of_each_run_normal)]
    average_value_average_normal = [float(sum(l))/len(l) for l in zip(*average_of_each_run_normal)]
    #Code to plot and save run results

    plot_all(dir_path, average_value_average_deviation, best_value_average_deviation, global_best_deviation, deviation_average, average_value_average_normal, best_value_average_normal, global_best_normal)

    save_best_individual(dir_path, "best_indiv_deviation.txt", global_best_individual_deviation)
    save_best_individual(dir_path, "best_indiv_normal.txt", global_best_individual_normal)

    save_best_runs(dir_path, "best_runs_deviation.txt", best_of_each_run_deviation)
    save_best_runs(dir_path, "best_runs_normal.txt", best_of_each_run_normal)

if __name__ == '__main__':
    main()
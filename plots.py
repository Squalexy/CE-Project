#Script responsible for plotting the data

import fnmatch
import os
import matplotlib.pyplot as plt
import csv

def plot_graph(data, color, label):
    plt.plot(data, color=color, label=label)

def plot_all(path, average_value_average_deviation, best_value_average_deviation, global_best_deviation, arr_avg_deviation, average_value_average_normal, best_value_average_normal, global_best_normal):
    
    plot_graph(average_value_average_deviation, 'red', 'Average Fitness')
    plot_graph(best_value_average_deviation, 'blue', 'Average Best Fitness')
    plot_graph(global_best_deviation, 'green', 'Best Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over generations with self adaptive deviation')
    plt.yscale('log')
    plt.legend()
    plt.savefig(path + "/fitness_graph_deviation.png")
    
    plt.figure()
    plot_graph(average_value_average_normal, 'red', "Average Fitness")
    plot_graph(best_value_average_normal, 'blue', 'Average Best Fitness')
    plot_graph(global_best_normal, 'green', 'Best Fitness')

    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over generations without self adaptive deviation')
    plt.yscale('log')
    plt.legend()
    plt.savefig(path + "/fitness_graph_normal.png")

    plt.figure()
    plot_graph(arr_avg_deviation, "orange", "Average Deviation")

    plt.xlabel('Generation')
    plt.ylabel('Deviation')
    plt.title('Deviation over generations')
    plt.legend()
    plt.savefig(path + "/deviation_graph.png")


def plot_all_box(arr_avg_fitness, arr_avg_best_fitness, arr_best_fitness):
    plt.boxplot([arr_avg_fitness, arr_avg_best_fitness, arr_best_fitness])
    plt.xticks([1, 2, 3], ['Average Fitness', 'Average Best Fitness', 'Best Fitness'])
    plt.xlabel('Fitness Category')
    plt.ylabel('Fitness')
    plt.title('Box Plots of Fitness')

def countFiles(dir_path):
    count = len(fnmatch.filter(os.listdir(dir_path), '*'))
    return count

def makeDir(parent_dir, number_of_files):
    directory = str(number_of_files)
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    return path


def save_best_individual(path, file_name, indiv):
    f = open(path + "/" + file_name, "w")
    f.write("array: " + str(indiv.value_arr) + "\n")
    f.write("fitness : " + str(indiv.fitness) + "\n")
    f.write("end_deviation: " + str(indiv.deviation) + "\n")
    f.write("lb: " + str(indiv.lb) + "\n")
    f.write("ub: " + str(indiv.ub) + "\n")
    f.close()
    pass


def save_to_CSV(filename, data):
    with open(filename, 'w', newline='') as csvfile:

        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Run', 'Average Fitness', 'Average Best Fitness', 'Best Fitness'])


def makeConfigFile(file_name, path, function_name, n_runs, number_generations, array_length, n_individuals, init_deviation, offset_mutation, mutation_prob, crossover_prob):
    f = open(path + "/" + file_name, "w")
    f.write("Optimization problem: " + function_name + "\n")
    f.write("number runs: " + str(n_runs) + "\n")
    f.write("number generations: " + str(number_generations) + "\n")
    f.write("array_size: " + str(array_length) + "\n")
    f.write("number_individuals: " + str(n_individuals) + "\n")
    f.write("initial_deviation: " + str(init_deviation) + "\n")
    f.write("offset_mutation: " + str(offset_mutation) + "\n")
    f.write("mutation probability: " + str(mutation_prob) + "\n")
    f.write("crossover probability: " + str(crossover_prob) + "\n")
    f.close()

def save_best_runs(path, file_name, data):
    f = open(path + "/" + file_name, "w")
    for val in data:
        f.write(str(min(val)) + "\n")
    f.close()
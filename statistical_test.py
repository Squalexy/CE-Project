import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import os

# obtain data
def get_data(filename):
    data = np.loadtxt(filename)
    return data

def describe_data(data):
    """ data is a numpy array of values"""
    min_ = np.amin(data)
    max_ = np.amax(data)
    mean_ = np.mean(data)
    median_ = np.median(data)
    mode_ = st.mode(data)
    std_ = np.std(data)
    var_ = np.var(data)
    skew_ = st.skew(data)
    kurtosis_ = st.kurtosis(data)
    q_25, q_50, q_75 = np.percentile(data, [25,50,75])
    basic = 'Min: %s\nMax: %s\nMean: %s\nMedian: %s\nMode: %s\nVar: %s\nStd: %s'
    other = '\nSkew: %s\nKurtosis: %s\nQ25: %s\nQ50: %s\nQ75: %s'
    all_ = basic + other
    print(all_ % (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75))
    return (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75)

def test_normal_sw(data):
    """Shapiro-Wilk"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.shapiro(norm_data)

def t_test_ind(data1,data2, eq_var=True):
    """
    parametric
    two samples
    independent
    """
    t,pval = st.ttest_ind(data1,data2, equal_var=eq_var)
    return (t,pval)

def mann_whitney(data1,data2):
    """
    non parametric
    two samples
    independent
    """    
    return st.mannwhitneyu(data1, data2)

def box_plot(data, title, vert=True):

    fig, ax = plt.subplots(figsize=(20,12))
    ax.set_title(f"{title} boxplots")
    ax.set_xlabel("Experience")
    ax.set_ylabel("Fitness")
    bp = ax.boxplot(data, patch_artist=True)
    colors = ['#0000FF', '#00FF00']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    plt.savefig(f"Plots/boxplot/boxplot_{title}.png")
    plt.close()
    
""" def histogram(data,title,xlabel,ylabel, optimization_problem, lb, ub, experiment, bins=30):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, range=(min(data), max(data)))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(range(1, bins+1))

    
    plt.text(0.95, 0.95, f"{optimization_problem}\nlb={lb}\nub={ub}", transform=plt.gca().transAxes,
             fontsize=8, fontweight='semibold', color='black', va='top', ha='right')
    plt.savefig("Plots/histogram/experiment"+str(experiment))
    
def histogram_norm(data,title,xlabel,ylabel,optimization_problem, lb, ub, experiment,bins=20):
    plt.figure()
    plt.hist(data,bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    min_,max_,mean_,median_,mode_,var_,std_,*X = describe_data(data)
    x = np.linspace(min_,max_,1000)
    pdf = st.norm.pdf(x,mean_,std_)
    plt.text(0.95, 0.95, f"{optimization_problem}\nlb={lb}\nub={ub}", transform=plt.gca().transAxes,
             fontsize=8, fontweight='semibold', color='black', va='top', ha='right')
    plt.plot(x,pdf,'r')    
    plt.savefig("Plots/histogram/experiment"+str(experiment)) """
    
def main():
    
    number_folders = []
    
    # replace this path with another one
    path = "Plots/experiments"
    
    if not os.path.exists("Plots/histogram"):
        os.mkdir("Plots/histogram")
        
    if not os.path.exists("Plots/boxplot"):
        os.mkdir("Plots/boxplot")
    
    for f in os.scandir(path):
        number_folders.append(f.path)
        
    file_count = 0
    datas = []
    
    for folder in number_folders:
        
        deviation_file = os.path.join(folder, "best_runs_deviation.txt")
        normal_file = os.path.join(folder, "best_runs_normal.txt")
        config_file = os.path.join(folder, "Config.txt")
        
        with open (config_file, 'r') as f:
            for line in f:
                if line.startswith("Optimization problem:"):
                    optimization_problem = line.split(":")[1].strip()
                if line.startswith("lb:"):
                    lb = line.split(":")[1].strip()
                if line.startswith("ub:"):
                    ub = line.split(":")[1].strip()

        deviation_data = get_data(deviation_file)
        normal_data = get_data(normal_file)
        datas.append(normal_data)
        datas.append(deviation_data)
        
        
        
        print("\n--------------------------------")
        print(f"Optimization problem: {optimization_problem}")
        print(f"{lb} to {ub}")
        
        # ---- normality test
        shapiro_deviation = test_normal_sw(deviation_data)
        shapiro_normal = test_normal_sw(normal_data)
        print(f"Shapiro deviation: {shapiro_deviation}\nShapiro normal: {shapiro_normal}")
        
        if (shapiro_normal[1] > 0.05 and shapiro_deviation[1] > 0.05):
            print("Normality test passed!\n Proceeding to do Homogeneity of Variance test...\n")
            stat, p = st.levene(deviation_data, normal_data)
            print(f"Stat: {stat}\nP-value: {p}\n")
            if (p > 0.05):
                print("Homogeneity test passed!\n Since there's interval data and there's independence, we can do a t-test!\n Proceeding to do t-test...\n")
                t , pval = t_test_ind(deviation_data, normal_data)
                print('t= %f   p = %s' % (t, pval))
            else:
                print("Homogeneity test failed!\n Data is non-parametric!\n Proceeding to do Mann-Whitney test...\n")
                u, pval = mann_whitney(deviation_data, normal_data)
                print('u= %f   p = %s' % (u, pval))
            
        else:
            print("Normality test failed!\n Data is non-parametric!\n Proceeding to do Mann-Whitney test...\n")
            u, pval = mann_whitney(deviation_data, normal_data)
            print('u= %f   p = %s' % (u, pval))
            
        print("--------------------------------\n")
        
        """ histogram(deviation_data, "Deviation data", "Num generations", "Fitness", optimization_problem, lb, ub, file_count)
        histogram(normal_data, "Normal data", "Num generations", "Fitness", optimization_problem, lb, ub, file_count + 1) 
        file_count += 2"""
        
        box_plot(deviation_data, f"{optimization_problem}_{ub}dev")
        box_plot(normal_data, f"{optimization_problem}_{ub}no_dev")
        
    box_plot(datas[0:4], "Ackley")
    box_plot(datas[4:8], "Griewangk")
    box_plot(datas[8:12], "Rastrigin")
    
    box_plot(datas[0:2], "Ackley_150")
    box_plot(datas[2:4], "Ackley_5.12")
    box_plot(datas[4:6], "Griewangk_150")
    box_plot(datas[6:8], "Griewangk_5.12")
    box_plot(datas[8:10], "Rastrigin_150")
    box_plot(datas[10:12], "Rastrigin_5.12")
        
if __name__ == "__main__":
    main()
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

def box_plot(data, labels):
    plt.boxplot(data,labels=labels)
    plt.show()
    
def histogram(data,title,xlabel,ylabel, optimization_problem, lb, ub, bins=25):
    plt.hist(data,bins=bins)
    plt.title(title)
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)
    
    plt.text(0.95, 0.95, f"{optimization_problem}\nlb={lb}\nub={ub}", transform=plt.gca().transAxes,
             fontsize=8, fontweight='semibold', color='black', va='top', ha='right')
    plt.show()
    
def histogram_norm(data,title,xlabel,ylabel,bins=20):
    plt.hist(data,normed=1,bins=bins)
    plt.title(title)
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)
    min_,max_,mean_,median_,mode_,var_,std_,*X = describe_data(data)
    x = np.linspace(min_,max_,1000)
    pdf = st.norm.pdf(x,mean_,std_)
    plt.plot(x,pdf,'r')    
    plt.show()
    
def main():
    
    number_folders = []
    
    # replace this path with another one
    path = "Plots\Alexy"
    
    for f in os.scandir(path):
        number_folders.append(f.path)
    
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
        
        # ---- describe data
        """ describe_data(deviation_data)
        describe_data(normal_data) """
    
        # ---- statistical tests
        t, pval = t_test_ind(deviation_data, normal_data)
        print('t= %f   p = %s' % (t, pval))
        
        u, pval = mann_whitney(deviation_data, normal_data)
        print('u= %f   p = %s' % (u, pval))
        
        histogram(deviation_data, "Deviation data", "Num generations", "Fitness", optimization_problem, lb, ub)
        histogram(normal_data, "Normal data", "Num generations", "Fitness", optimization_problem, lb, ub)

if __name__ == "__main__":
    main()
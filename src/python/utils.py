import os
import time
import numpy as np
from scipy.stats import uniform
from prettytable import PrettyTable

def uniform_random(sample_size, interval = (0, 1)):
    rng = np.random.default_rng()
    pvalues = uniform.rvs(size=sample_size, random_state=rng)
    interval_range = interval[1] - interval[0]

    return pvalues * interval_range + interval[0]


def find_closest(array, value):
    # looking for closest value and its index in array
    idx = (np.abs(array-value)).argmin()
    return idx, array[idx]

def interval_freqs(sample, intervals):
    '''
    intervals - list of tuples
    sample - list
    return intervals, freqs
    '''
    num_intervals = len(intervals)
    freqs = [0]*num_intervals
    for value in sample:
        for i in range(num_intervals):
            interval = intervals[i]
            if value >= interval[0] and value < interval[1]:
                freqs[i] += 1
    return intervals, freqs

def results_traverse(path = '/mnt/d/Data/pvals/pvals', endswith='.pval'):
    '''
    generator of filepaths with endswith - wll be used with endswith='.pval' with files of pvals
    '''
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(endswith) or endswith == '*':
                pvals_file = os.path.join(root, file)
                yield pvals_file

def read_pvalues(path):
    '''
    read floats from file and return list of pvals
    file consist of floats one per line
    '''
    # read pvalues from file
    times = []
    times.append(time.time())
    with open(path, 'r') as f:
        content = f.readlines()
    times.append(time.time())
    # pvals = np.array([float(x) for x in content])
    pvals = [float(x) for x in content]
    # pvals = np.loadtxt(content, dtype=np.float32) numpy is slower than built in float()
    times.append(time.time())
    # print(times)
    return pvals


def data_to_csv(header, rows, filename='test.csv'):
    table = PrettyTable(header)
    table.add_rows(rows)
    assert len(header) == len(rows[0]), print(len(header), len(rows[0]))
    with open('test.csv', 'w', newline='') as f_output:
        f_output.write(table.get_csv_string())

if __name__ == "__main__":
    # Reading pvalues as using numpy
    pvals = read_pvalues(path='/mnt/d/Data/pvals/pvals/dieharder/pvals/Dieharder(0) Diehard Birthdays Test.pval')
    print(f"first 3 pvals{pvals[:3]}, last 3 pvals{pvals[-3:]}\n")

    # Reading pvalues as using generator
    paths = list(results_traverse(path = '/mnt/d/Data/pvals/pvals', endswith='.pval'))
    print(*paths[:2],sep='\n')

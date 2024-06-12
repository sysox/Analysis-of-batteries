import os
import numpy as np
from scipy.stats import kstest, uniform

def open_or_create(file_path):
    if os.path.exists(file_path):
        return open(file_path, 'a')
    return open(file_path, 'w')

def find_closest(array, value):
    # looking for closest value and its index in array
    idx = (np.abs(array-value)).argmin()
    return idx, array[idx]

def multinomial_coeffs(lst):
    res, i = 1, sum(lst)
    i0 = lst.index(max(lst))
    for a in lst[:i0] + lst[i0+1:]:
        for j in range(1,a+1):
            res *= i
            res //= j
            i -= 1
    return res



def results_traverse(path = '/mnt/d/Data/pvals/pvals', endswith='*'):
    # r=root, d=directories, f = files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(endswith) or endswith == '*':
                pvals_file = os.path.join(root, file)
                yield pvals_file




def uniform_random(sample_size, interval = (0, 1)):
    rng = np.random.default_rng()
    pvalues = uniform.rvs(size=sample_size, random_state=rng)
    return pvalues
#     TODO change to general interval not (0,1)

def histogram(values, bin_edges, probs = None, sort_needed = True):
    if sort_needed:
        values = np.array(values)
        if probs is not None:
            sort_idx = np.argsort(values)
            sorted_values = list(values[sort_idx])
            probs = np.array(probs)
            probs = list(probs[sort_idx])
        else:
            sorted_values = sorted(values)

    y = [0]*(len(bin_edges)+1)
    idx = 0
    for i, val in enumerate(sorted_values):
        while(idx != len(bin_edges) and val >= bin_edges[idx]):
            idx += 1
        if probs is not None:
            y[idx] += probs[i]
        else:
            y[idx] += 1

            # if idx > len(bin_edges) - 1:
                #     print(f"value {val} not in bin_edges {bin_edges[-3:]}")
    # print(y)
    return (bin_edges, y)

def interval_freqs(sample, intervals, sort_needed = False):
    if sort_needed:
        sorted_sample = sorted(sample)
    num_intervals = len(intervals)
    freqs = [0]*num_intervals

    for value in sample:
        for i in range(num_intervals):
            interval = intervals[i]
            if value >= interval[0] and value < interval[1]:
                freqs[i] += 1

    return intervals, freqs


if __name__ == "__main__":
    # for file in results_traverse(endswith='.pval'):
    #     print(file)
    # print(histogram([0.1, 0.2, 0.3, 0.4], bin_edges=[0.33, 0.66, 1.1], weights=None))
    print(histogram([0.1, 0.2, 0.3, 0.4], bin_edges = [0, 0.33, 0.66], probs=[0.25, 0.25, 0.25, 0.25]))
    #
    # print(KS_test_scipy([0.1, 0.23, 0.77], what_to_return = 1))
    # print(KS_test_scipy([0.1, 0.23, 0.77], what_to_return=3))
    histogram([1.0000000000000002], bin_edges = np.arange(0, 100)/100)
from bisect import bisect_left, bisect_right
import numpy as np
from collections import Counter
from utils import uniform_random, find_closest, intervals_and_freqs, read_pvalues
def bin_frequency_inefficient(array, interval, interval_type="(]" ):
    '''
    computes frequency of interval in sorted_array
    interval - tuple of (a,b)
    interval_type - string "()", "[)", "(]", "[]"
    '''
    freq = 0
    a,b = interval
    if interval_type == '[]':
        for val in array:
            if val >= a and val <= b:
                freq += 1

    if interval_type == '(]':
        for val in array:
            if val > a and val <= b:
                freq += 1
    if interval_type == '[)':
        for val in array:
            if val >= a and val < b:
                freq += 1
    if interval_type == '()':
        for val in array:
            if val > a and val < b:
                freq += 1
    return freq

def bin_frequency(sorted_array, interval, interval_type="(]" ):
    '''
    computes frequency of interval in sorted_array
    interval - tuple of (a,b)
    interval_type - string "()", "[)", "(]", "[]"
    '''

    a,b = interval
    if interval_type[0] == '(':
        idx1 = bisect_right(sorted_array, a)
    else:
        idx1 = bisect_left(sorted_array, a)

    if interval_type[1] == ')':
        idx2 = bisect_left(sorted_array, b)
    else:
        idx2 = bisect_right(sorted_array, b)

    # print(idx1, idx2)
    return idx2 - idx1

def histogram_inefficient(unsorted_sample, num_bins=None, limits=None, domain = (0,100)):
    if num_bins is not None:
        limits = (np.arange(num_bins)) / num_bins
    intervals =  [(limits[i], limits[i+1]) for i in range(len(limits)-1)]
    if limits[0] > domain[0]:
        intervals = [(domain[0], limits[0])] + intervals
    if limits[-1] < domain[1]:
        intervals.append((limits[-1], domain[1]))
    bins, freqs = intervals_and_freqs(unsorted_sample, intervals)
    starts, ends = zip(*bins)
    assert sum(freqs) == len(unsorted_sample), print(sum(freqs), len(unsorted_sample))
    return dict(zip(starts, freqs))

def histogram_unsorted(unsorted_sample, num_bins=None, limits=None):
    '''
    compute histogram for unsorted sample in O(n), limits has to be sorted
    if provided num_bins it will creat bins for (0,1) interval
    i.e. (-0.1,0.1), (0.1,0.2), ..., (0.9,infinity)  ... for num_bins=10
    result dict -0.1: freq of x<0.1, 0.1: freq -0.1<x<0.1,..., freq for x> 0.9
    '''

    if  num_bins is not None:
        limits = (np.arange(num_bins)) / num_bins
    else:
        limits = sorted(limits)
    l = len(limits)
    indices = [bisect_right(limits, d) for d in unsorted_sample]
    freqs = Counter(indices)
    hist = dict(zip(range(l), [0]*l) )

    for idx, freq in freqs.items():
        hist[idx-1] = freqs[idx]
    hist = dict(zip(limits, hist.values()))
    assert sum(hist.values()) == len(unsorted_sample), print(sum(hist.values()), len(unsorted_sample))
    return hist
def histogram_sorted(sample, num_bins=None, limits=None, domain = (0,1) ):
    '''
    compute histogram for sorted sample in O(log n), limits does not have to be sorted
    if provided num_bins it will creat bins for (0,1) interval
    i.e. (-infinity,0.1], (0.1,0.2], ..., (0.9,infinity)  ... for num_bins=10
    '''

    if  num_bins is not None:
        limits = (np.arange(num_bins)) / num_bins
    if limits[0] > domain[0]:
        limits = [domain[0]] + limits

    indices = [bisect_left(sample, d) for d in limits]
    # print(indices)
    freqs =  list(np.array(indices[1:]) - np.array(indices[:-1]))
    freqs.append(len(sample) - indices[-1])
    hist = dict(zip(limits, freqs))
    assert sum(hist.values()) == len(sample), print(sum(hist.values()), len(sample))
    return hist
    # last  = bisect_left(sample, limits[-1])

def find_equal_bins(sorted_sample, depth):
    '''
    split sample into bins of equal size
    '''
    print(depth, len(sorted_sample))
    idx = len(sorted_sample) // 2

    val1 = sorted_sample[idx]
    val2 = sorted_sample[idx+1]

    idx1, idx2 = bisect_left(sorted_sample, val1), bisect_right(sorted_sample, val1)
    idx3, idx4 = bisect_left(sorted_sample, val2), bisect_right(sorted_sample, val2)
    i = find_closest(np.array([idx1, idx2, idx3, idx4]), idx)
    val, idx = [val1, val2, val1, val2][i], [idx1, idx2, idx3, idx4][i]

    if depth == 1:
        return [val]
    else:
        vals_left = find_equal_bins(sorted_sample[:idx], depth-1)
        vals_right = find_equal_bins(sorted_sample[idx:], depth-1)
        return vals_left + [val] + vals_right

def find_equal_bins(sorted_sample, num_bins):
    pass

def select_equiv(sorted_sample, num_bins, values = True):
    step = (len(sorted_sample)-1) / (num_bins-1)
    idxs = []
    for i in range(num_bins):
        idx = round(step * i)
        idxs.append(idx)

    if values == True:
        res = [float(sorted_sample[idx]) for idx in idxs]
        return res
    else:
        return idxs


if __name__ == "__main__":
    # histogram of (0,1) sample for unsorted and sorted sample
    # sample = uniform_random(5)
    # sample[2] = 1
    # sample[1] = 0
    # hist0 = histogram_inefficient(sample, num_bins=5)
    # hist1 = histogram_unsorted(sample, num_bins=5)
    # hist2 = histogram_sorted(sorted(sample), num_bins=5)
    #
    # print(f"sample={sorted(sample)}\n histogram unsing histogram_unsorted={hist1}")
    # print(f"sample={sorted(sample)}\n histogram unsing histogram_unsorted={hist1}")
    # print(f"sample={sorted(sample)}\n histogram unsing histogram_sorted={hist2}\n")
    # assert hist0 == hist1, print(hist0, hist1)
    # assert hist1 == hist2, print(hist1, hist2)
    #
    # # bin_frequency testing
    sorted_array = [1, 1, 2, 2, 3]
    # closed_freq = bin_frequency(sorted_array, (1, 2), interval_type="[]")
    # left_open_freq = bin_frequency(sorted_array, (1, 2), interval_type="(]")
    # right_open_freq = bin_frequency(sorted_array, (1, 2), interval_type="[)")
    # open_freq = bin_frequency(sorted_array, (1, 2), interval_type="()")
    # print(f"closed_freq={closed_freq}, left_open_freq={left_open_freq}, right_open_freq={right_open_freq}, open_freq={open_freq}\n")
    #
    # # find_equal_bins
    # sorted_sample = sorted(uniform_random(100))
    # limits = find_equal_bins(sorted_sample, depth=3)
    # print(limits)
    # hist1 = histogram_sorted(sorted_sample, limits=limits)
    # hist2 = histogram_inefficient(sorted_sample, limits=limits)
    # # print(histogram_unsorted(sorted_sample, limits=limits)) TODO
    # print(len(hist1), hist1)
    # assert histogram_sorted(sorted_sample, limits=limits) == histogram_inefficient(sorted_sample, limits=limits)

    #
    # path = '/mnt/d/Data/batteries_testing/1st/dieharder/Dieharder(10) Diehard Parking Lot Test.pval'
    # pvals = read_pvalues(path)
    # find_equal_bins(pvals, depth=10)

    # print(bisect_left(sorted_array, 2))
    # print(bisect_right(sorted_array, 2))
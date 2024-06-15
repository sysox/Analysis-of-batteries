from bisect import bisect_left, bisect_right
import numpy as np
from collections import Counter
from utils import uniform_random
def histogram_unsorted(unsorted_sample, num_bins=10, limits=None):
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
    assert sum(hist.values()) == len(unsorted_sample)
    return hist
def histogram_sorted(sample, num_bins=10, limits=None):
    '''
    compute histogram for sorted sample in O(log n), limits does not have to be sorted
    if provided num_bins it will creat bins for (0,1) interval
    i.e. (-infinity,0.1), (0.1,0.2), ..., (0.9,infinity)  ... for num_bins=10
    '''
    if  num_bins is not None:
        limits = (np.arange(num_bins + 2)) / num_bins
    indices = [bisect_left(sample, d) for d in limits[:-1]]
    # print(indices)
    freqs =  list(np.array(indices[1:]) - np.array(indices[:-1]))
    freqs[-1] += bisect_right(sample, limits[-1]) - indices[-1]
    hist = dict(zip(limits[:], freqs ))
    assert sum(hist.values()) == len(sample)
    return hist
    # last  = bisect_left(sample, limits[-1])

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

if __name__ == "__main__":
    # histogram of (0,1) sample for unsorted and sorted sample
    sample = uniform_random(4)
    sample[2] = 1
    sample[1] = 0
    hist1 = histogram_unsorted(sample, num_bins=10)
    hist2 = histogram_sorted(sorted(sample), num_bins=10)
    print(f"sample={sorted(sample)}\n histogram unsing histogram_unsorted={hist1}")
    print(f"sample={sorted(sample)}\n histogram unsing histogram_sorted={hist2}\n")
    assert hist1 == hist2

    #
    sorted_array = [1, 1, 2, 2, 3]
    closed_freq = bin_frequency(sorted_array, (1, 2), interval_type="[]")
    left_open_freq = bin_frequency(sorted_array, (1, 2), interval_type="(]")
    right_open_freq = bin_frequency(sorted_array, (1, 2), interval_type="[)")
    open_freq = bin_frequency(sorted_array, (1, 2), interval_type="()")
    print(f"closed_freq={closed_freq}, left_open_freq={left_open_freq}, right_open_freq={right_open_freq}, open_freq={open_freq}\n")

import copy, math

from scipy.stats import kstest, chisquare, normaltest, binom_test


    # https://homes.luddy.indiana.edu/kapadia/project2/node14.html

def KS_scipy_uniform(sample):
    res = kstest(sample, 'uniform')
    return res.statistic, res.pvalue
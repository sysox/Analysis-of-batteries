#tests
from scipy.stats import normaltest, binomtest
from scipy.stats import chisquare, chi2_contingency
from scipy.stats import kstest, ks_2samp

#distributions
from scipy.stats import uniform, norm
from utils import uniform_random

from histograms import histogram_inefficient, bin_frequency
from collections import namedtuple
import mock, math, time, json
from collections import defaultdict
from utils import results_traverse
from C_functions import GoF_pvals_wrapper
from names import GoF_test_ids#, uniform_pvals_WSL_path, uniform_pvals_Windows_path

def transform_pvalue(pvalue = 0.5, src_alternative = 'greater', dst_alternative = 'two-sided'):
    '''tranform pvalue computed for (one , or two tailed test) sample p-value to '''
    if src_alternative == dst_alternative: #[less -> less], [greater -> greater], [two-sided -> two-sided]
        return pvalue
    if dst_alternative == 'two-sided':      #[less -> 'two-sided'], [greater -> 'two-sided']
        return 2*min(pvalue, 1-pvalue)

    if set([src_alternative, dst_alternative]) == set(['less', 'greater']):     #[less -> greater], [greater -> less]
        return 1-pvalue

    if  src_alternative == 'two-sided':
        return [pvalue/2, 1-pvalue/2] # choose one based on additional aspects

def KS_scipy(sample, cdf=uniform.cdf, alternative='greater'):
    '''
    :return res.statistic, res.pvalue for KS uniformity test
    '''
    res = kstest(sample, cdf= cdf, alternative=alternative)
    return res
def KS_2samp_scipy(sample1, sample2, alternative='greater'):
    '''
    :return res.statistic, res.pvalue for KS uniformity test
    '''
    res = ks_2samp(sample1, sample2, alternative=alternative)
    return res
def chisquare_scipy(f_obs, f_exp = None):
    res = chisquare(f_obs, f_exp=f_exp)
    return res
def chisquare_2sample_scipy(f_obs1, f_obs2):
    tmp = chi2_contingency([f_obs1, f_obs2])
    res = mock.Mock()
    res.statistic, res.pvalue = tmp[:2]
    return res

def binom_scipy(f_obs, n_obs, p = None, f_exp=None, n_exp=None, alternative='two-sided'):
    if p == None:
        p = f_exp/n_exp
    res = binomtest(f_obs, n=n_obs, p=p, alternative=alternative)
    return res

def binom_as_normal_scipy(freq_obs, p, n):
    mean = n * p
    std = math.sqrt(n * p * (1 - p))
    pvalue_right = norm.sf(x=freq_obs, loc=mean, scale=std)
    return 2*min(pvalue_right, 1-pvalue_right)

# uniformity tests from batteries or other C code
def NIST_proportion(pvals, sorted=False, ALPHA = 0.01):
    '''
    see assess.c taken from NIST STS 2.1.2
    rewritten into python
    if ( c < ALPHA )
        count++;
    passCount = sampleSize - count;
	p_hat = 1.0 - ALPHA;
	proportion_threshold_max = (p_hat + 3.0 * sqrt((p_hat*ALPHA)/sampleSize)) * sampleSize;
	proportion_threshold_min = (p_hat - 3.0 * sqrt((p_hat*ALPHA)/sampleSize)) * sampleSize;
	if ( (passCount < proportion_threshold_min) || (passCount > proportion_threshold_max))
        fprintf(summary, "%4d/%-4d *  %s\n", passCount, sampleSize, testNames[test]);
    '''
    sampleSize = len(pvals)
    if sorted == False:
        pvals = sorted(pvals)
    count = bin_frequency(pvals, interval=(0, ALPHA), interval_type="[]")
    passCount = sampleSize - count
    res = mock.Mock()
    res.proportion = passCount/sampleSize
    p_hat = 1 - ALPHA
    proportion_threshold_max = (p_hat + 3.0 * math.sqrt((p_hat * ALPHA) / sampleSize)) * sampleSize
    proportion_threshold_min = (p_hat - 3.0 * math.sqrt((p_hat * ALPHA) / sampleSize)) * sampleSize
    if ((passCount < proportion_threshold_min) or (passCount > proportion_threshold_max)):
        res.passed = False
    else:
        res.passed = True
    return res





if __name__ == "__main__":
    # data
    sample1 = uniform_random(10)
    sample2 = uniform_random(100)
    hist1 = histogram_inefficient(sample1, num_bins=10)
    hist2 = histogram_inefficient(sample2, num_bins=10)
    freqs1 = list(hist1.values())
    freqs2 = list(hist2.values())

    # KS test
    res_KS = KS_scipy(sample1)
    print(f"KS statistic = {res_KS[0]}, pvalue = {res_KS[1]}")

    # KS 2 sample test
    res_KS2 = KS_2samp_scipy(sample1, sample2)
    print(f"KS 2 sample statistic = {res_KS2.statistic}, pvalue = {res_KS2.pvalue}")

    # chisq test
    res_chisq = chisquare_scipy(freqs1)
    print(f"chisq statistic = {res_chisq.statistic}, pvalue = {res_chisq.pvalue}")

    # chisq 2sample test
    res_chisq2 = chisquare_2sample_scipy(freqs1, freqs2)
    print(f"chisq 2 sample statistic = {res_chisq2.statistic}, pvalue = {res_chisq2.pvalue}")

    # binom test
    res_binom = binom_scipy(freqs2[0], n_obs=100, p=None, f_exp=1, n_exp=10)
    print(f"binom pvalue = {res_binom.pvalue}")
    res_binom = binom_scipy(freqs2[0], n_obs=100, p=0.1)
    print(f"binom pvalue = {res_binom.pvalue}")

    #calling C code uniformity test
    simulated_pvals = GoF_pvals_wrapper(src_pvals_filepath = '../../data/uniform_pvals_devurand.pval',
                                        dst_pvals_filepath = 'tmp',
                                        sample_size = 10, repetitions = 1000, GoF_idx = 0, seed=1)
    # simulated_pvals = list(map(float, open('tmp', 'r').readlines()))

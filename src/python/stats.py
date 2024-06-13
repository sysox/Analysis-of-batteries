import numpy as np
import math, collections

from scipy.stats import binom, norm, chi2, uniform, kstwobign, multinomial
from scipy.stats import chisquare, kstest,  binomtest

def binomial_as_normal_dist(n=100, p=0.5):
    '''
    normal approximation for binomial distribution
    returns:
        observation points (0, 1, ..., n)
        binomial: pmf, cdf
        normal (approx of binomial): mean, std, pdf, cdf
    '''
    x_disc = np.arange(0, n + 1, 1)
    binom_pmf = [binom.pmf(x, n=n, p=p) for x in x_disc]
    binom_cdf = [binom.cdf(x, n=n, p=p) for x in x_disc]
    # checking whether cdf corresponds to sum
    for i in x_disc:
        assert abs(binom_cdf[i] - sum(binom_pmf[:i + 1])) < 10 ** (-10), print(binom_cdf[i], binom_pmf[:i + 1])

    mean = n * p
    std = math.sqrt(n * p * (1 - p))
    norm_pdf = norm.pdf(x_disc, mean, std)
    norm_cdf = norm.cdf(x_disc, mean, std)
    res = {'x': x_disc, 'mean': mean, 'std': std, 'binom_pmf': binom_pmf, 'binom_cdf': binom_cdf, 'norm_pdf': norm_pdf,
           'norm_cdf': norm_cdf}
    return res
def decompose(target_sum, target_len, pool, subset=[], repeat = False):
    '''
    generator all possible subsets of pool of length target_len
    with sum(subset) == target_sum
    '''
    if sum(subset) == target_sum and len(subset) == target_len:
        yield subset
    if sum(subset) > target_sum or len(subset) > target_len:
        return
    for idx in range(len(pool)):
        tmp_subset = subset + [pool[idx]]
        if repeat == False:
            yield from  decompose(target_sum, target_len, pool[idx:], tmp_subset, repeat=repeat)
        else:
            yield from  decompose(target_sum, target_len, pool, tmp_subset, repeat=repeat)
        tmp_subset = tmp_subset[:-1]
def chi2_dist(Expected_freqs_vec):
    '''
    for expected frequencies vector compute for possible observations (Observed_freqs_vec):
      multinomial probabilities of thei occurence
      chi2_stat and corresponding p-value
      !!! chi2_stat (float) is multiplied by constant (product of expected frequencies) and represented as int
        int is used to merge outcomes with the same chi2_stat to event and sume their probs
    return chi2_stats_ints, multinomial_probs, chi2_pvals, observations
    '''
    c = math.prod(Expected_freqs_vec)
    n = sum(Expected_freqs_vec)
    k = len(Expected_freqs_vec)
    df = k - 1
    observations = list(decompose(n, k, range(n+1), subset=[], repeat = True))
    # print(observations)
    multinomial_probs = multinomial(n, [1/k]*k).pmf(observations)
    assert abs(sum(multinomial_probs) - 1) < 10 ** (-10), sum(multinomial_probs) - 1
    chi2_stats = []
    chi2_pvals = []
    for Observed_freqs_vec in observations:
        Power_divergenceResult = chisquare(f_obs=Observed_freqs_vec, f_exp=Expected_freqs_vec)
        statistic, pvalue = Power_divergenceResult.statistic, Power_divergenceResult.pvalue
        chi2_stats.append(statistic)
        chi2_pvals.append(pvalue)
    chi2_stats_ints = [round(chi2_stat*c) for chi2_stat in chi2_stats]
    return chi2_stats_ints, multinomial_probs, chi2_pvals, observations

def multinomial_as_chi2_dist(n, k):
    '''
    chi2 approximation for multinomial distribution
    returns:
        observation points chi2_stats (not chi2_stats_ints)
        multinomial: pmf, cdf with events equal to chi2_stats
            - probabilities of observation are summed
            (i.e. if observations produce same chi2 stat e.g. if expected - observed are [0,0,0,2] and [1,1,1,1] )
            then their probabilities are summed in pm
        chi2 (approx of multinomial): pdf, cdf
    '''
    df = k - 1
    Expected_freqs_vec = [n//k]*k
    stat_prob_pvals_obs = zip(*chi2_dist(Expected_freqs_vec))
    stat_prob_pvals_obs = sorted(stat_prob_pvals_obs, key=lambda x: x[0])
    chi2_stats_ints, probs, chi2_pvals, observations = zip(*stat_prob_pvals_obs)
    chi2int_hist = collections.Counter(chi2_stats_ints)
    chi2int_hist = dict(sorted(chi2int_hist.items()))
    c = math.prod(Expected_freqs_vec)
    # x_obs = np.arange(chi2_stats_ints)/c
    x_events = [ chi2statint/c for chi2statint in chi2int_hist.keys()]
    idx = 0
    chi2_as_multinomial_pmf = []
    for chi2stat_int, freq in chi2int_hist.items():
        event_prob = sum(probs[idx: idx + freq])
        chi2_as_multinomial_pmf.append(event_prob)
        idx += freq
    chi2_as_multinomial_cdf = [sum(chi2_as_multinomial_pmf[:idx+1]) for idx in range(len(chi2_as_multinomial_pmf))]
    chi2_pdf = chi2.pdf(x_events,df=df)
    chi2_cdf = chi2.cdf(x_events,df=df)
    for i in range(len(x_events)):
        assert abs(chi2_as_multinomial_cdf[i] - sum(chi2_as_multinomial_pmf[:i + 1])) < 10 ** (-10), print(chi2_as_multinomial_cdf[i], chi2_as_multinomial_pmf[:i + 1])
    res = {'x':x_events, 'chi2_disc_pmf':chi2_as_multinomial_pmf,
           'chi2_disc_cdf':chi2_as_multinomial_cdf,
           'chi2_pdf': chi2_pdf, 'chi2_cdf':chi2_cdf}
    return res

if __name__ == "__main__":
    # distribution binomial and approx normal
    binom_data = binomial_as_normal_dist(n=100, p=0.5)
    print(f"sum from cdf= {binom_data['binom_cdf'][-1]}, sum using pmf= {sum(binom_data['binom_pmf'])}")
    print(f"sum from cdf= {binom_data['norm_cdf'][-1]}, sum using pdf= {sum(binom_data['norm_pdf'])}")
    # !!! surprinsingly sum of normal distribution for distrete values is close 1!!!

    # distribution multinomial and approx chi2
    chi2_data = multinomial_as_chi2_dist(n = 24, k=4)
    print(f"sum from cdf= {chi2_data['chi2_disc_cdf'][-1]}, sum using pmf= {sum(chi2_data['chi2_disc_pmf'])}")
    print(f"sum from cdf= {chi2_data['chi2_cdf'][-1]}, sum using pdf= {sum(chi2_data['chi2_pdf'])}")
    # !!! surprinsingly sum of chi2 distribution for distrete values is not close to 1
    # - does not make sense to integrate for discrete points!!!




import prettytable
# scipy functions meaning:
# rvs
# pmf - probability mass function (discrete distribution)
# pdf - probability density function (continuous)
# cdf - cumulative distribution function (both discrete and continuous); ppf - inverse of cdf
# sf = 1 - cdf - sometimes more accurate; isf - inverse of sf


# norm.pdf(x_axis, loc = 0, scale = 1)  - normal dist loc = \mu, scale = sigma
# chi2.pdf(x_axis, df=4)                - chi2 dist
# binom.pmf(x_axis, n=n, p=p)           - binomial dist (k, n, p)
# expon.pdf(x_axis, scale = 1/lambda)   - exponential dist
# uniform.pdf(x_axis)                   - loc = 0, scale = 1 [loc, scale]
# kstwobign.cdf(x_axis)
# multinomial.pmf([3, 4], n=7, p=[0.4, 0.6])

# np.histogram(a, bins=10, range=None, density=None, weights=None)

# x_axis = np.arange(-1, 1, 0.1)  - values range step 0.01 <=> np.linspace(-1,1,20)
# np.cumsum([1, 2, 3])            - cumulative sum [1, 3, 6]




def multinomial_coeffs(lst):
    res, i = 1, sum(lst)
    i0 = lst.index(max(lst))
    for a in lst[:i0] + lst[i0+1:]:
        for j in range(1,a+1):
            res *= i
            res //= j
            i -= 1
    return res


def uniform_random(sample_size, interval = (0, 1)):
    rng = np.random.default_rng()
    pvalues = uniform.rvs(size=sample_size, random_state=rng)
    interval_range = interval[1] - interval[0]

    return pvalues * interval_range + interval[0]

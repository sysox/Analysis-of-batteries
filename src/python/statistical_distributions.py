#tests
from scipy.stats import binom, norm, chi2, uniform, multinomial, ksone

#distributions
from scipy.stats import chisquare
from scipy.special import smirnov

import collections, copy, math, matplotlib.pyplot as plt, numpy as np
from src.python.histograms import bin_frequency


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
def normal_distributions(n=400, p=0.5, alpha=0.01, alternative="two-sided"):
    # Percent point function (inverse of cdf — percentiles).
    x_disc = np.arange(0, n + 1, 1)
    mean = n * p
    std = math.sqrt(n * p * (1 - p))
    pdf = norm.pdf(x_disc, mean, std)
    cdf = norm.cdf(x_disc, mean, std)
    x_range = (norm.ppf(10 ** (-4), mean, std), norm.ppf(1 - 10 ** (-4), mean, std))
    print(x_range)
    distribution_absolute = {'x': x_disc, 'mean': mean, 'std': std, 'pdf': pdf, 'cdf': cdf, 'ymax': max(pdf)}

    tail_alpha = alpha / 2 if alternative == "two-sided" else alpha
    if alternative == "less" or alternative == "two-sided":
        x_right_critical = norm.ppf(1 - tail_alpha, mean, std)
        y_right_critical = norm.pdf(x_right_critical, mean, std)
        assert abs(norm.cdf(x_right_critical, mean, std) - (1 - tail_alpha)) < 10 ** (-10), print(
            norm.cdf(x_right_critical, mean, std), (1 - tail_alpha))

        distribution_absolute['x_right_critical'] = x_right_critical
        distribution_absolute['y_right_critical'] = y_right_critical

    if alternative == "greater" or alternative == "two-sided":
        x_left_critical = norm.ppf(tail_alpha, mean, std)
        y_left_critical = norm.pdf(x_left_critical, mean, std)
        distribution_absolute['x_left_critical'] = x_left_critical
        distribution_absolute['y_left_critical'] = y_left_critical
        assert abs(norm.cdf(x_left_critical, mean, std) - tail_alpha) < 10 ** (-10), print(
            norm.cdf(x_left_critical, mean, std), tail_alpha)

    distribution_relative = {k: v / n for k, v in distribution_absolute.items()}

    distribution_absolute['x_range'] = x_range
    distribution_relative['x_range'] = (distribution_absolute['x_range'][0] / n, distribution_absolute['x_range'][1] / n)

    funcs_absolute = {'pdf': lambda x: norm.pdf(x, mean, std), 'cdf': lambda x: norm.cdf(x, mean, std),
                      'ppf': lambda x: norm.ppf(x, mean, std), 'x': lambda x: x}
    funcs_relative = {'pdf': lambda x: norm.pdf(x, mean, std) / n, 'cdf': lambda x: norm.cdf(x, mean, std) / n,
                      'ppf': lambda x: norm.ppf(x, mean, std) / n, 'x': lambda x: x / n}
    return {'distribution_absolute': distribution_absolute,
            'distribution_relative': distribution_relative,
            'funcs_absolute': funcs_absolute,
            'funcs_relative': funcs_relative}

dists = {'uniform': uniform, 'normal': norm, 'chi2': chi2}
class ECDF:
    '''
    taken from https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.smirnov.html#scipy.special.smirnov
    '''
    def __init__(self, x, cdf=uniform.cdf):
        self.cdf = cdf
        self.n = len(x)
        self.x = self.quantiles = sorted(copy.copy(x))
        self.ecdf_values = np.array([])
        self.Dn_value, self.Dn_minus_value, self.Dn_plus_value = None, None, None
        self.KS_pvalue = None


    def Dn_plus(self):
        if self.Dn_plus_value != None:
            return self.Dn_plus_value
        if self.ecdf_values.size == 0:
            self.ecdf_values = np.arange(self.n+1, dtype=float) / self.n

        self.Dn_plus_array = self.ecdf_values[1:] - self.cdf(self.x) # i/N - U_i, i=1,...,N
        self.Dn_plus_index = np.argmax(self.Dn_plus_array, axis=0)
        self.Dn_plus_value = self.Dn_plus_array[self.Dn_plus_index]
        self.Dn_plus_x = self.x[self.Dn_plus_index]


        return self.Dn_plus_value
    def Dn_minus(self):
        if self.Dn_minus_value != None:
            return self.Dn_minus
        if self.ecdf_values.size == 0:
            self.ecdf_values = np.arange(self.n+1, dtype=float) / self.n
        self.Dn_minus_array = self.cdf(self.x) - self.ecdf_values[:-1] # U_i - (i-1)/N , i=1,...,N
        self.Dn_minus_index = np.argmax(self.Dn_minus_array, axis=0)
        self.Dn_minus_value = self.Dn_minus_array[self.Dn_minus_index]
        self.Dn_minus_x = self.x[self.Dn_minus_index]
        return self.Dn_minus_value

    def Dn(self):
        if self.Dn_value != None:
            return self.Dn_value
        if self.Dn_plus_value == None:
            self.Dn_plus()
        if self.Dn_minus_value == None:
            self.Dn_minus()
        self.Dn_value = max(self.Dn_plus_value, self.Dn_minus_value)
        return self.Dn_value
    def ecdf(self, t):
        return bin_frequency(self.x, interval=(0, t), interval_type="[]")

    def KS(self):
        if self.KS_pvalue != None:
            return self.KS_pvalue
        self.KS_pvalue = smirnov(self.n, self.Dn())
        return self.KS_pvalue


    def plot(self,  domain=(0,1), ax=None, label=None, xticks=np.array([]), yticks=np.array([]), xlabels=np.array([])):
        if xticks.size == 0:
            xticks = np.concatenate(([domain[0]], self.x, [domain[1]]))
        if yticks.size == 0:
            yticks = np.concatenate((self.ecdf_values, [domain[1]]))

        if xlabels.size == 0:
            xlabels = [f'{x:1.2f}' for x in xticks]

        ax.step(xticks,yticks, where='post', label='Empirical CDF', color='black', linewidth=0.5)

        x = np.linspace(domain[0], domain[1], 100)
        ax.plot(x, self.cdf(x), '--', label=label, color='g')

        x_plus = self.Dn_plus_x
        y_plus_min = self.cdf(x_plus)
        y_plus_max = y_plus_min + self.Dn_plus_value
        ax.vlines([x_plus], [y_plus_min], [y_plus_max], color='magenta', lw=4,
                   label='$D_n^+$=' + f"{self.Dn_plus_value:1.4f}")
        ax.vlines([x_plus], [0], [y_plus_max], color='magenta', lw=1, linestyle='--')

        x_minus = self.Dn_minus_x
        y_minus_max = self.cdf(x_minus)
        y_minus_min = y_minus_max - self.Dn_minus_value

        ax.vlines([x_minus], [y_minus_min], [y_minus_max], color='cyan', lw=4,
                   label='$D_n^-$=' + f"{self.Dn_minus_value:1.4f}")
        ax.vlines([x_minus], [0], [y_minus_max], color='cyan', lw=1, linestyle='--')
        xticks, yticks = [x_minus, x_plus], [y_minus_min, y_plus_max]
        ax.set_xticks(ticks=xticks, labels=[f"{xtick:1.2f}" for xtick in xticks])
        # ax2 = ax.twiny()
        # ax2.set_xticks(ticks=[0, 1], labels=['0', '1'])
        # ax.grid(True)
        # plt.plot([], [], ' ', label=f"D-={self.Dn_minus_value:1.2f}\nD+={self.Dn_plus_value:1.2f}")
        ax.legend(framealpha=0.5, shadow=False, fontsize="8", loc = "upper left")

    def __str__(self):
        return f"ECDF: sample={self.x_sorted}, ecdf_values={self.ecdf_values}"


if __name__ == "__main__":
    # ecdf of uniform (0, 1) and its plot
    sample = uniform.rvs(size=100)
    U01 = ECDF(sample)
    U01.Dn()
    fig, ax = plt.subplots(1, 1, layout='constrained')
    U01.plot(domain=(0, 1), ax=ax,  label="Uniform(0, 1)")
    plt.show()

    # distribution binomial and approx normal
    binom_data = binomial_as_normal_dist(n=100, p=0.5)
    print(f"sum from cdf= {binom_data['binom_cdf'][-1]}, sum using pmf= {sum(binom_data['binom_pmf'])}")
    print(f"sum from cdf= {binom_data['norm_cdf'][-1]}, sum using pdf= {sum(binom_data['norm_pdf'])}")
    # !!! surprinsingly sum of normal distribution for distrete values is close 1!!!

    # distribution multinomial and approx chi2
    chi2_data = multinomial_as_chi2_dist(n = 24, k=4)
    print(f"sum from cdf= {chi2_data['chi2_disc_cdf'][-1]}, sum using pmf= {sum(chi2_data['chi2_disc_pmf'])}")
    print(f"sum from cdf= {chi2_data['chi2_cdf'][-1]}, sum using pdf= {sum(chi2_data['chi2_pdf'])}")
    # !!! surprisingly sum of chi2 distribution for distrete values is not close to 1
    # - does not make sense to integrate for discrete points!!!

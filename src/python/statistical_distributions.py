from scipy.stats import ksone, chi2, binom_test, norm, uniform
from  scipy.special import smirnov
from scipy import stats
import numpy as np
import copy, math, matplotlib.pyplot as plt
from utils import bin_frequency



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


    def plot(self, fig, ax, domain=(0,1), label=None, xticks=np.array([]), yticks=np.array([]), xlabels=np.array([])):
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
        plt.vlines([x_plus], [y_plus_min], [y_plus_max], color='magenta', lw=4,
                   label='$D_n^+$=' + f"{self.Dn_plus_value:1.6f}")
        plt.vlines([x_plus], [0], [y_plus_max], color='magenta', lw=1, linestyle='--')

        x_minus = self.Dn_minus_x
        y_minus_max = self.cdf(x_minus)
        y_minus_min = y_minus_max - self.Dn_minus_value

        plt.vlines([x_minus], [y_minus_min], [y_minus_max], color='cyan', lw=4,
                   label='$D_n^-$=' + f"{self.Dn_minus_value:1.6f}")
        plt.vlines([x_minus], [0], [y_minus_max], color='cyan', lw=1, linestyle='--')
        xticks, yticks = [x_minus, x_plus], [y_minus_min, y_plus_max]
        ax.set_xticks(ticks=xticks, labels=[f"{xticks[0]:1.2f}", f"{xticks[1]:1.2f}"])


        # ax.grid(True)
        # plt.plot([], [], ' ', label=f"D-={self.Dn_minus_value:1.2f}\nD+={self.Dn_plus_value:1.2f}")
        ax.legend(framealpha=1, shadow=True)

    def __str__(self):
        return f"ECDF: sample={self.x_sorted}, ecdf_values={self.ecdf_values}"


if __name__ == "__main__":
    # ecdf of uniform (0, 1) and its plot
    sample = uniform.rvs(size=100)
    U01 = ECDF(sample)
    U01.Dn()
    fig, ax = plt.subplots(1, 1, layout='constrained')
    U01.plot(fig=fig, ax=ax, domain=(0, 1), label="Uniform(0, 1)")
    plt.show()


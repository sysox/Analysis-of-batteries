import numpy as np
import matplotlib.pyplot as plt
from statistical_distributions import ECDF
from utils import uniform_random

def draw_hist(freqs, expected_freq, axis, text):
    colors = ['g' if freq > expected_freq else 'r' for freq in freqs]
    freqs = np.array(freqs)
    ylow, ymax = min(freqs), max(freqs)

    axis.bar(np.arange(len(freqs)) + 1,freqs-expected_freq, color=colors, width=0.5, bottom=expected_freq)
    axis.set_ylim(ylow, ymax)
    axis.set_title(text)
    yticks_abs = np.array([ylow, expected_freq, ymax])
    ylabels_abs = list(map(str, yticks_abs))
    axis.set_yticks(ticks=yticks_abs, labels=ylabels_abs, minor=False)

    axis2 = axis.twinx()

    yticks_rel = yticks_abs/expected_freq
    ylabels_rel = list(map(str, map(lambda x: f"{x:.2f}", yticks_rel)))
    axis2.set_ylim(ymin=yticks_rel[0], ymax=yticks_rel[-1])
    axis2.set_yticks(ticks=yticks_rel, labels=ylabels_rel, minor=False)

    axis.hlines(y=expected_freq, xmin=1, xmax=len(freqs), colors='b', linestyles='dashed')

def draw_ECDF(values, axis, text):
    ecdf = ECDF(values)
    ecdf.KS()
    ecdf.plot(domain=(0,1), ax=axis, label=text)

def draw_KS_relative(values, axis, text):
    #ecdf.ecdf_values, ecdf.Dn_value, ecdf.Dn_minus_value, ecdf.Dn_plus_value, ecdf.KS_pvalue
    ecdf = ECDF(values)
    ecdf.KS()
    y = ecdf.Dn_plus_array
    n = len(y)
    index_min, index_max = np.argmin(y), np.argmax(y)
    ymin, ymax = y[index_min], y[index_max]
    x = np.arange(1, n+1)
    print(len(y), len(x))
    ecdf_data_min, ecdf_data_max = min(y), max(y)
    color = ['g' if yval > 0 else 'r' for yval in y ]
    axis.set_ylim(ymin=ymin*1.1, ymax=ymax*1.1)
    axis.set_xlim(xmin=+0.5, xmax=n+0.5)
    axis.set_xticks([1,index_min, index_max, n])
    axis.set_yticks(([0, ymin, ymax]))
    axis.scatter(x, y, s=2, color = color)
    axis.hlines(y=0, xmin=1, xmax=n+1, colors='b', linestyles='dashed')

def draw_tails(tails, axis, text):
    y = np.array(tails)
    x = np.arange(len(y))-len(y)//2
    ymin, ymax = min(y), max(y)
    xmin, xmax = min(x), max(x)
    color = ['g' if yval > 1 else 'r' for yval in y ]

    axis.set_ylim(ymin=ymin*1.1, ymax=ymax*1.1)
    axis.set_xlim(xmin=xmin-0.5, xmax=xmax+0.5)
    axis.set_yticks(([1, ymin, ymax]))
    axis.set_xticks(x)
    axis.scatter(x, y, s=2, color = color)
    axis.vlines(x=0, ymin=ymin, ymax=ymax, colors='b', linestyles='dashed')


if __name__ == '__main__':

    fig, axs = plt.subplots(2, 2)

    # bar histogram
    draw_hist(freqs=[1, 2, 3, 4, 5], expected_freq=3, axis=axs[0][0], text="uniformity")

    # ECDF
    pvals = uniform_random(10)
    draw_ECDF(values=pvals, axis=axs[0][1], text="Uniform(0, 1)")

    # KS
    pvals = uniform_random(100)
    draw_KS_relative(values=pvals, axis=axs[1][0], text="Uniform(0, 1)")

    # tails
    tails = uniform_random(9)
    tails[4] = 1
    draw_tails(tails=tails, axis=axs[1][1], text="tails")

    fig.tight_layout()
    plt.show()
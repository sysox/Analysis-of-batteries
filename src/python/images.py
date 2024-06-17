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

def draw_KS(freqs, expected_freq, axis, text):
    pass

def draw_tails(freqs, expected_freq, axis, text):
    pass

if __name__ == '__main__':

    fig, axs = plt.subplots(2, 2)
    # bar histogram
    draw_hist(freqs=[1, 2, 3, 4, 5], expected_freq=3, axis=axs[0][0], text="uniformity")
    # ECDF
    pvals = uniform_random(10)
    draw_ECDF(values=pvals, axis=axs[0][1], text="uniformity")



    fig.tight_layout()
    plt.show()
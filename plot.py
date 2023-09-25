
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def univ_plot(dataset, x, kde=True):
    fig, axs = plt.subplots(
        nrows=2,
        figsize=(8, 4),
        gridspec_kw={'height_ratios': [1, 3]})

    sns.histplot(dataset, x=x, kde=True, ax=axs[1])
    axs[1].axvline(x=x.mean(), color='darkred', linestyle='--')
    axs[1].axvline(x=x.median(), color='darkgreen', linestyle='--')
    sns.boxplot(x=x, ax=axs[0], showmeans=True, color='purple')

    plt.show()

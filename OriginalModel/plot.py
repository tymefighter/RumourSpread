import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math

def plot_degree_distribution(
    degree_distribution, max_degree, 
    title, xlabel='degree', ylabel='frequency'
):
    plt.plot(degree_distribution[:max_degree + 1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def get_axis(axes, idx, num_rows, num_plots_per_row):

    if num_rows == 1 and num_plots_per_row == 1:
        return axes
    elif num_rows == 1 or num_plots_per_row == 1:
        return axes[idx]
    else:
        return axes[idx // num_plots_per_row][idx % num_plots_per_row]

def plot_bit_counts(
    bit_counts_list, title_list, 
    suptitle, num_plots_per_row=2,
    xlabel='', ylabel=''
):
    num_rows = (len(bit_counts_list) + num_plots_per_row - 1) // num_plots_per_row
    fig, axes = plt.subplots(
        nrows=num_rows, ncols=num_plots_per_row, figsize=(16, 9)
    )

    for idx, bit_counts in enumerate(bit_counts_list):

        ax = get_axis(axes, idx, num_rows, num_plots_per_row)

        num_bit_strings = len(bit_counts[0])
        num_bits = int(math.log2(num_bit_strings))
        bit_string_list = [None] * num_bit_strings

        for i in range(num_bit_strings):
            bit_string_list[i] = f'{i:0{num_bits}b}'

        bit_count_df = pd.DataFrame(
            data=np.array(bit_counts).T, index=bit_string_list
        )

        sns.heatmap(bit_count_df, ax=ax, cmap='viridis')
        ax.set_title(title_list[idx])

    for j in range(idx + 1, num_rows * num_plots_per_row):
        fig.delaxes(
            get_axis(axes, j, num_rows, num_plots_per_row)
        )

    fig.suptitle(suptitle)
    fig.text(0.5, 0.04, xlabel, ha='center')
    fig.text(0.04, 0.5, ylabel, va='center', rotation='vertical')
    plt.show()

def plot_range_of_info_spread(
    range_of_info_spread_list, 
    title_list, suptitle,
    num_plots_per_row=2,
    xlabel='Timestep', ylabel='Binary String'
):  
    plot_bit_counts(range_of_info_spread_list, title_list, 
        suptitle, num_plots_per_row,
        xlabel, ylabel)

def plot_opinion_fragmentation(
    opinion_freq_list, 
    title_list, suptitle,
    num_plots_per_row=2,
    xlabel='Timestep', ylabel='Binary String'
):
    plot_bit_counts(opinion_freq_list, title_list, 
        suptitle, num_plots_per_row,
        xlabel, ylabel)

def plot_avg_info_entropy(
    avg_entropy_list, label_list, 
    title, xlabel='Timestep', ylabel='Average Entropy'
):
    for i in range(len(avg_entropy_list)):
        plt.plot(avg_entropy_list[i], label=label_list[i])

    plt.title(title)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

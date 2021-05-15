import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math

def plot_degree_distribution(degree_distribution, max_degree):
    
    plt.plot(degree_distribution[:max_degree + 1])
    plt.show()

def plot_bit_counts(bit_counts_list, title_list):

    num_rows = (len(bit_counts_list) + 1) // 2
    fig, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(12, 8))

    for idx, bit_counts in enumerate(bit_counts_list):

        ax = axes[idx % 2] if num_rows == 1 else axes[idx // 2][idx % 2]

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

    if len(bit_counts_list) % 2 == 1:
        fig.delaxes(
            axes[1] if num_rows == 1 else axes[len(bit_counts_list // 2)][1]
        )

    plt.show()

def plot_range_of_info_spread(
    range_of_info_spread_list, 
    title_list
):  
    plot_bit_counts(range_of_info_spread_list, title_list)

def plot_opinion_fragmentation(
    opinion_freq_list, 
    title_list
):
    plot_bit_counts(opinion_freq_list, title_list)

def plot_avg_info_entropy(
    avg_entropy_list, label_list, 
    title
):
    for i in range(len(avg_entropy_list)):
        plt.plot(avg_entropy_list[i], label=label_list[i])

    plt.title(title)
    plt.legend()
    plt.show()

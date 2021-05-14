import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math

def plot_degree_distribution(degree_distribution, max_degree):
    
    plt.plot(degree_distribution[:max_degree + 1])
    plt.show()

def plot_bit_counts(bit_counts, title):

    num_bit_strings = len(bit_counts[0])
    num_bits = int(math.log2(num_bit_strings))
    bit_string_list = [None] * num_bit_strings

    for i in range(num_bit_strings):
        bit_string_list[i] = f'{i:0{num_bits}b}'

    bit_count_df = pd.DataFrame(
        data=np.array(bit_counts).T, index=bit_string_list
    )

    sns.heatmap(bit_count_df)
    plt.title(title)
    plt.show()

def plot_range_of_info_spread(
    range_of_info_spread, title='Range of Info Spread'
):  
    plot_bit_counts(range_of_info_spread, title)

def plot_opinion_fragmentation(opinion_freq, title='Opinion Frequency'):

    plot_bit_counts(opinion_freq, title)

def plot_avg_info_entropy(avg_entropy):

    plt.plot(avg_entropy)
    plt.show()

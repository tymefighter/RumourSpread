import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import seaborn as sns
from rumour_spread_info_extract import RumourSpreadModel
from callback import (
    OpinionFragmentation,
    AverageInformationEntropy,
    Adversary
)

NUM_NODES = 1000
NUM_BITS = 5
NODE_CAPACITY = 100
ALPHA = 0.040
BETA = 0.900
GAMMA = 0.060
DELTA_IN = 20.0
DELTA_OUT = 20.0
INIT_NUM_NODES = 10
NUM_PROPAGATORS = 10
TIMESTEPS = 2001

def plot_avg_info_entropy(
    avg_entropy, 
    title, xlabel='Timestep', ylabel='Average Entropy'
):
    plt.plot(avg_entropy)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_opinion_fragmentation(bit_counts, title):
    num_bit_strings = len(bit_counts[0])
    num_bits = int(math.log2(num_bit_strings))
    bit_string_list = [None] * num_bit_strings

    for i in range(num_bit_strings):
        bit_string_list[i] = f'{i:0{num_bits}b}'

    bit_count_df = pd.DataFrame(
        data=np.array(bit_counts).T, index=bit_string_list
    )

    sns.heatmap(bit_count_df, cmap='viridis')
    plt.title(title)
    plt.xlabel('Timestep')
    plt.ylabel('Binary String')
    plt.show()

def plot_histogram(val_arr, bins, title, xlabel, ylabel):

    plt.hist(val_arr, bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def main():
    while True:
        inp_string = input('Enter: ')

        if inp_string == 'done':
            break
        
        conservation_factor, confidence_factor, adversary_nodes = \
            map(float, inp_string.split())

        rumour_spread = RumourSpreadModel(
            NUM_NODES, NUM_BITS, NODE_CAPACITY,
            conservation_factor, confidence_factor,
            INIT_NUM_NODES, ALPHA, BETA, GAMMA, DELTA_IN, DELTA_OUT
        )

        graph = rumour_spread.get_graph()
        outdegree = np.array(graph.compute_outdegrees())
        init_nodes = np.random.choice(
            NUM_NODES, size=NUM_PROPAGATORS, 
            replace=False, p=outdegree / np.sum(outdegree)
        )
        init_propagators = dict([(node, 0) for node in init_nodes])

        callback_list = [
            AverageInformationEntropy(
                NUM_NODES, TIMESTEPS
            ),
            OpinionFragmentation(
                NUM_NODES, NUM_BITS, TIMESTEPS
            ),
            Adversary(0, int(adversary_nodes), 1000)
        ]

        [average_entropy, opinion_freq, _], node_entropy_list, edge_entropy_list = \
            rumour_spread.simulate(
                init_propagators, TIMESTEPS, callback_list, 
                [1000, 2000], [(500, 1000), (1500, 2000)]
            )

        plot_opinion_fragmentation(
            opinion_freq, 
            f'K = {conservation_factor}, β = {confidence_factor}'
        )

        plot_avg_info_entropy(
            average_entropy,
            f'K = {conservation_factor}, β = {confidence_factor}', 
            xlabel='Timestep', ylabel='Average Entropy'
        )

        plot_histogram(
            node_entropy_list[0], 50, 
            'Node Entropy Distribution (Before Adversary)',
            'Node Entropy', 'Probability'
        )

        plot_histogram(
            node_entropy_list[1], 50, 
            'Node Entropy Distribution (After Adversary)',
            'Node Entropy', 'Probability'
        )

        plot_histogram(
            edge_entropy_list[0], 50, 
            'Edge Entropy Distribution (Before Adversary)',
            'Edge Entropy', 'Probability'
        )

        plot_histogram(
            edge_entropy_list[1], 50, 
            'Edge Entropy Distribution (After Adversary)',
            'Edge Entropy', 'Probability'
        )

if __name__ == '__main__':
    main()


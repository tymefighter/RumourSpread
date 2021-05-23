import numpy as np
from rumour_spread_info_extract import RumourSpreadModel
from callback import (
    RangeOfInformationSpread,
    OpinionFragmentation,
    AverageInformationEntropy,
    Adversary
)
from plot import (
    plot_range_of_info_spread,
    plot_opinion_fragmentation,
    plot_avg_info_entropy,
    plot_histogram
)
import sys

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

def main():
    conservation_factor, confidence_factor = map(float, sys.argv[1:3])
    adversary_nodes = int(sys.argv[3])
    argument_string = f'K = {conservation_factor}, ' \
        + f'β = {confidence_factor}, r = {adversary_nodes}'

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
        Adversary(0, adversary_nodes, 1000)
    ]

    [avg_entropy, opinion_freq, _], node_entropy_list, edge_entropy_list = \
        rumour_spread.simulate(
            init_propagators, TIMESTEPS, callback_list, 
            [1000, 2000], [(500, 1000), (1500, 2000)]
        )

    plot_opinion_fragmentation(
        [opinion_freq], [argument_string], 'Opinion Fragmentation',
        num_plots_per_row=1
    )
    plot_avg_info_entropy([avg_entropy], [argument_string], 'Average Entropy')
    
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


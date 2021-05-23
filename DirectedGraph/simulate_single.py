import numpy as np
from rumour_spread_model import RumourSpreadModel
from callback import (
    RangeOfInformationSpread,
    OpinionFragmentation,
    AverageInformationEntropy,
    Adversary
)
from plot import (
    plot_range_of_info_spread,
    plot_opinion_fragmentation,
    plot_avg_info_entropy
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
TIMESTEPS = 1000
ADVERSARY_TIMESTEP = 500

def main():
        
    conservation_factor, confidence_factor = map(float, sys.argv[1:3])
    adversary_nodes = int(sys.argv[3])
    argument_string = f'K = {conservation_factor}, ' \
        + f'β = {confidence_factor}, r = {adversary_nodes}'

    rumour_spread = RumourSpreadModel(
        NUM_NODES, NUM_BITS, NODE_CAPACITY,
        conservation_factor, confidence_factor,
        INIT_NUM_NODES, ALPHA, BETA, GAMMA, DELTA_IN, DELTA_OUT,
        plot_degree_dist=False
    )

    callback_list = [
        AverageInformationEntropy(
            NUM_NODES, TIMESTEPS
        ),
        OpinionFragmentation(
            NUM_NODES, NUM_BITS, TIMESTEPS
        ),
        RangeOfInformationSpread(
            NUM_NODES, NUM_BITS, TIMESTEPS
        )
    ]

    if adversary_nodes > 0:
        callback_list.append(
            Adversary(0, adversary_nodes, ADVERSARY_TIMESTEP)
        )

    graph = rumour_spread.get_graph()
    outdegree = np.array(graph.compute_outdegrees())
    init_nodes = np.random.choice(
        NUM_NODES, size=NUM_PROPAGATORS, 
        replace=False, p=outdegree / np.sum(outdegree)
    )
    init_propagators = dict([(node, 0) for node in init_nodes])

    callback_results = \
        rumour_spread.simulate(init_propagators, TIMESTEPS, callback_list)

    avg_entropy, opinion_freq, range_of_info_spread = callback_results[:3]

    plot_avg_info_entropy([avg_entropy], [argument_string], 'Average Entropy')
    plot_opinion_fragmentation(
        [opinion_freq], [argument_string], 'Opinion Fragmentation',
        num_plots_per_row=1
    )
    plot_range_of_info_spread(
        [range_of_info_spread], [argument_string], 'Range of Information',
        num_plots_per_row=1
    )

if __name__ == '__main__':
    main()


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
    plot_avg_info_entropy,
    plot_degree_distribution
)
from scale_free import generate_scale_free

NUM_NODES = 3000
NUM_BITS = 5
NODE_CAPACITY = 320
ALPHA = 0.010
BETA = 0.970
GAMMA = 0.020
DELTA_IN = 40.0
DELTA_OUT = 40.0
INIT_NUM_NODES = 100
NUM_PROPAGATORS = 10
TIMESTEPS = 2000

def get_center_window(outdegrees, window_size):

    outdegree_pairs = list(enumerate(outdegrees))
    sorted(outdegree_pairs, key=lambda x: x[0])

    n = len(outdegree_pairs)
    center_idx = n // 2

    return [
        node for _, node in 
        outdegree_pairs[max(center_idx - window_size, 0): 
            min(center_idx + window_size, n - 1)]
    ]

def main():

    graph = generate_scale_free(
        NUM_NODES, INIT_NUM_NODES, 
        ALPHA, BETA, GAMMA, DELTA_IN, DELTA_OUT
    )

    scc = graph.scc()
    print(f'Number of SCC: {len(scc)}')
    # print(f'Diameter: {graph.compute_diameter(check_inf=True)}')

    plot_degree_distribution(
        graph.compute_outdegree_distribution(), 
        int(0.08 * NUM_NODES),
        'Outdegree Distribution'
    )

    plot_degree_distribution(
        graph.compute_indegree_distribution(), 
        int(0.08 * NUM_NODES),
        'Indegree Distribution'
    )

    # confidence_factor_list = [0.5, 1.0, 3.0]
    # conservation_factor_list = [0, 0.5, 1., 3., 5.]

    confidence_factor_list = [1.0]
    conservation_factor_list = [0]

    for confidence_factor in confidence_factor_list:
        
        m = len(conservation_factor_list)

        suptitle = f'β = {confidence_factor}'
        title_list = [None] * m
        range_of_info_spread_list = [None] * m
        opinion_freq_list = [None] * m
        avg_entropy_list = [None] * m

        for i, conservation_factor in enumerate(conservation_factor_list):
            title_list[i] = f'K = {conservation_factor}'

            rumour_spread = RumourSpreadModel(
                NUM_NODES, NUM_BITS, NODE_CAPACITY,
                conservation_factor, confidence_factor,
                INIT_NUM_NODES, ALPHA, BETA, GAMMA, DELTA_IN, DELTA_OUT,
                plot_degree_dist=False
            )

            graph = rumour_spread.get_graph()
            outdegree = np.array(graph.compute_outdegrees())
            # init_nodes = np.random.choice(
            #     NUM_NODES, size=NUM_PROPAGATORS, 
            #     replace=False, p=outdegree / np.sum(outdegree)
            # )
            init_nodes = get_center_window(outdegree, 4)
            init_propagators = dict([(node, 0) for node in init_nodes])

            range_of_info_spread_list[i], opinion_freq_list[i], avg_entropy_list[i], _ = \
                rumour_spread.simulate(init_propagators, TIMESTEPS, [
                    RangeOfInformationSpread(
                        NUM_NODES, NUM_BITS, TIMESTEPS
                    ),
                    OpinionFragmentation(
                        NUM_NODES, NUM_BITS, TIMESTEPS
                    ),
                    AverageInformationEntropy(
                        NUM_NODES, TIMESTEPS
                    ),
                    Adversary(
                        0, 100, 500
                    )]
                )

        plot_avg_info_entropy(avg_entropy_list, title_list, 'Average Entropy, ' + suptitle)
        plot_opinion_fragmentation(
            opinion_freq_list, title_list, 'Opinion Fragmentation, ' + suptitle,
            num_plots_per_row=3
        )
        plot_range_of_info_spread(
            range_of_info_spread_list, title_list, 'Range of Information, ' + suptitle,
            num_plots_per_row=3
        )
        
if __name__ == '__main__':
    main()


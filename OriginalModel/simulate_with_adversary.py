from rumour_spread_model import RumourSpreadModel
from scale_free import generate_scale_free
from callback import (
    RangeOfInformationSpread,
    OpinionFragmentation,
    AverageInformationEntropy,
    Adversary
)

from plot import (
    plot_degree_distribution,
    plot_range_of_info_spread,
    plot_opinion_fragmentation,
    plot_avg_info_entropy
)

NUM_NODES = 1000
NUM_BITS = 5
NODE_CAPACITY = 100
INIT_NUM_NODES = 15
NUM_EDGES_PER_STEP = 10
TIMESTEPS = 1000

def main():

    graph =  generate_scale_free(NUM_NODES, INIT_NUM_NODES, NUM_EDGES_PER_STEP)
    plot_degree_distribution(
        graph.compute_degree_distribution(), 
        100,
        'degree distribution', 'degree'
    )
    print(f'Diameter {graph.compute_diameter()}')

    confidence_factor_list = [4.5, 3.0, 1.0]
    conservation_factor_list = [0, 0.5, 1.0, 3.0, 6.0, 10.0]

    # Curr Best: K = 1.0, β = 4.5
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
                INIT_NUM_NODES, NUM_EDGES_PER_STEP
            )

            _, range_of_info_spread_list[i], opinion_freq_list[i], avg_entropy_list[i] = \
                rumour_spread.simulate({0: 0}, TIMESTEPS, [
                    Adversary(0, 10, 500),
                    RangeOfInformationSpread(
                        NUM_NODES, NUM_BITS, TIMESTEPS
                    ),
                    OpinionFragmentation(
                        NUM_NODES, NUM_BITS, TIMESTEPS
                    ),
                    AverageInformationEntropy(
                        NUM_NODES, TIMESTEPS
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


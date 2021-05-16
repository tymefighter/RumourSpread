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

NUM_NODES = 500
NUM_BITS = 5
NODE_CAPACITY = 100
INIT_NUM_NODES = 20
NUM_EDGES_PER_STEP = 20
TIMESTEPS = 20

def main():

    plot_degree_distribution(
        generate_scale_free(NUM_NODES, INIT_NUM_NODES, NUM_EDGES_PER_STEP)
            .compute_degree_distribution(), 150
    )

    confidence_factor_list = [1]
    conservation_factor_list = [3.0]

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
                    Adversary(0, 100, 0),
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

        plot_range_of_info_spread(
            range_of_info_spread_list, title_list, suptitle,
            num_plots_per_row=2
        )
        plot_opinion_fragmentation(
            opinion_freq_list, title_list, suptitle,
            num_plots_per_row=2
        )
        plot_avg_info_entropy(avg_entropy_list, title_list, suptitle)

if __name__ == '__main__':
    main()


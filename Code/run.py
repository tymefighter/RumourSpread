from rumour_spread_model import RumourSpreadModel
from callback import RangeOfInformationSpread
from plot import plot_range_of_info_spread

def main():

    num_nodes = 3000
    num_bits = 5
    timesteps = 100
    
    rumour_spread = RumourSpreadModel(num_nodes, num_bits, 100, 1, 1)
    result_list = rumour_spread.simulate(
        {0: 0}, timesteps, 
        [RangeOfInformationSpread(
            num_nodes, num_bits, timesteps
        )]
    )

    plot_range_of_info_spread(result_list[0])

if __name__ == '__main__':
    main()


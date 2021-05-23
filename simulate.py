import argparse
import sys
import os

def build_parser():

    parser = argparse.ArgumentParser(
        description='Rumour Spread and Adversary Simulation Runner'
    ) 

    # Experiment Selection Arguments
    parser.add_argument('-o', '--original', dest='original',
        help='Run Original Model')

    parser.add_argument('-d', '--directed', dest='directed',
        help='Run Directed Graph Model')

    parser.add_argument('-i', '--information', dest='information',
        help='Run Node and Edge Information Entropy Computation')

    # Sub-Experiment or Experiment Parameter Selection Arguments
    parser.add_argument('-g', '--general', dest='general',
        help='Runs a general experiment - ' 
        + 'no specific values are to be provided here')

    parser.add_argument('-ga', '--general-adversary', dest='general_adversary',
        help='Run a general adversary experiment - '
        + 'no specific values are to be provided here')

    parser.add_argument('-cons', '--conservation', 
        dest='conservation', type=float,
        help='Conservation Parameter')

    parser.add_argument('-conf', '--confidence', 
        dest='confidence', type=float,
        help='Confidence Parameter')

    parser.add_argument('-numadv', '--num-adversary-nodes', 
        dest='num_adv', type=int,
        help='Number of Adverary Nodes')

    return parser

def main():

    parser = build_parser()
    args = parser.parse_args()

    if args.original:
        if args.general:
            os.system('python OriginalModel/simulate.py')

        elif args.general_adversary:
            os.system('python OriginalModel/simulate_with_adversary.py')

        else:
            os.system(
                'python OriginalModel/simulate_single.py '
                + f'{args.conservation} {args.confidence} {args.num_adv} '
            )
    
    elif args.directed:

        if args.general:
            os.system('python DirectedGraph/simulate.py')

        elif args.general_adversary:
            os.system('python DirectedGraph/simulate_with_adversary.py')

        else:
            os.system(
                'python DirectedGraph/simulate_single.py '
                + f'{args.conservation} {args.confidence} {args.num_adv} '
            )

    elif args.information:
        os.system(
            'python NodeAndEdgeInformation/simulate_info_extract.py '
            + f'{args.conservation} {args.confidence} {args.num_adv} '
        )

    else:
        print('Argument Error !')

if __name__ == '__main__':
    main()

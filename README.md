# Information Theoretic Adversarial Approach to Rumour Spread

This repository contains simulation code for the experiments
described in our paper, [rumour spread](rumour_spread.pdf).

## Installation

The necessary installation instructions are provided in [INSTALL.md](INSTALL.md).

## Running the Simulation

The simulation file is [simulation.py](simulation.py), it can be run using
a python interpretor. There are many command line arguments or flags which can 
be passed to this file.

### Help

One can pass the `-h` flag as a command line argument while running this file
to get information about all the arguments that this file supports.
```
python simulate.py -h
```

### A set of example uses are shown below:

1. Running the Original Model without Adversary
```
python simulate.py -o -g
```

2. Running the Original Model with parameters
```
python simulate.py -o -cons 0.5 -conf 4.5 -numadv 10
```

3.  Running the Directed Graph Model with Adversary
```
python simulate.py -d -ga
```

4. Running the Directed Graph Model with Adversary
```
python simulate.py --directed --general-adversary
```

5. Running the Node and Edge Information Computation
```
python simulate.py --information -cons 1 -conf 3 -numadv 10
```

## Directories

-   The experiments concerning the original rumour spread model are
    present in the `OriginalModel` directory of this repository.

-   The experiments concerning our modified (directed graph) version 
    of the model are present in the `DirectedGraph` directory of
    this repository.

-   The experiments concerning the measurement of the node and edge
    entropies at steady-state are present in the `NodeAndEdgeInformation`
    directory of this repository.

-   The documents relevant to our experimentation are provided in
    the `Documents` directory of this repository.

-   A faster experimental version of the simulation algorithm is
    present in the `FasterDirectedGraphExperimental` directory
    of this repository.

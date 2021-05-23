# OriginalModel

This directory contains the simulation code for the original model,
which is described briefly in our paper [rumour spread](../rumour_spread.pdf),
and in detail in this paper [original model](https://www.nature.com/articles/s41598-017-09171-8).
Also, our adversary simulation code for this model is also present in this directory.

The directory content is described as follows:

-   `graph.py`: This file contains the `Graph` class, which represents the Undirected
    Graph data structure. It also provides methods which implement various graph algorithms.
    This `Graph` class would be used as a model of the underlying undirected network of
    individuals in the original rumour spread model.

-   `scale_free.py`: This file contains code for generating an Undirected Scale-Free graph
    based on the Barabási-Albert algorithm. This details of this algorithm is present
    in the paper [Barabási-Albert](https://science.sciencemag.org/content/286/5439/509).

-   `queue_distort.py`: This file contains code for the `Queue` class which implements
    the FIFO queue data structure. An additional method provided by this `Queue` class
    is `update_first_occ`, which replaces the first occurrence (from the head of 
    the queue) of a value by another value. We did not use the in-built `collections.deque`
    data structure because it did not provide such a method.

-   `memory_queue.py`: This file contains code for the FIFO memory data structure, which
    represents the memory of an individual (i.e. node) in the graph. This provides methods
    for picking the most frequent binary string in the memory, distorting the first
    occurrence of a binary string in the memory, computing the entropy of the frequency
    distribution present in the memory, and more.

-   `prob.py`: This file contains code for the `Prob` class, which contains methods for
    computing the distortion and acceptance probabilities.

-   `rumour_spread_model.py`: This file contains code for the `RumourSpreadModel` class,
    which implements the entire rumour spreading simulation algorithm. It also provides
    a `Callback` class which allows for various callback objects to keep track of different
    metrics to be computed during the simulation, however one could develop callbacks which
    could modify the state of the simulation itself (for example: the Adversary !).

-   `callbacks.py`: This file contains code for the various callback classes which subclass the
    `Callback` class present in `rumour_spread_model.py`. The callback classes provided in this
    file are 
    1. `RangeOfInformationSpread`: It measures the range of information spread in the network.

    2. `OpinionFragmentation`: It measures the fragmentation of opinions in the network.

    3. `AverageInformationEntropy`: It computes the average information entropy over all the
        nodes' memories in the graph.

    4. `Adversary`: It implements the adversary we have designed for the original model

-   `plot.py`: This file contains code for several useful plotting functions - functions
    which plot the results produced by the `RangeOfInformationSpread`, `OpinionFragmentation`
    and `Adversary` callbacks.

Just an observation: The file descriptions given in this markdown are presented in a
topological order of the dependency graph of these files.
# Directed Graph Model

This directory contains the codes for the simulation of the directed graph version (described in our paper [rumour_spread](../rumour_spread.pdf)) of the original undirected graph model ([original model](https://www.nature.com/articles/s41598-017-09171-8)).

## Files Description

-   `graph.py`: It contains the `Graph` class, which represents the Directed
    Graph data structure. It also provides methods which implement some graph algorithms such as
    graph diameter finding algorithm, finding strongly connected components, etc.
    This `Graph` class is used as a model of the underlying directed network of
    individuals in the directed graph rumour spread model.

-   `scale_free.py`: This file contains code for generating a Directed Scale-Free graph. 
    The algorithm is described in the paper 
    [Directed Scale-Free Graph](http://jenniferchayes.com/Papers/dirSCgrph.pdf).
    Since the algorithm described in the above paper doesn't necessarily produces a strongly 
    connected graph, the code also merges the strongly connected components to produce the
    connected graph.

-   `queue_distort.py`: This file is same as 
    [OriginalModel/queue_distort.py](../OriginalModel/queue_distort.py), and described in     
    [OriginalModel/README.md](../OriginalModel/README.md).

-   `memory_queue.py`: This file is same as 
    [OriginalModel/memory_queue.py](../OriginalModel/memory_queue.py), and described in 
    detail in [OriginalModel/README.md](../OriginalModel/README.md).

-   `prob.py`: This file contains code for the `Prob` class, which contains methods for
    computing the distortion and acceptance probabilities. This file is same as
    [OriginalModel/prob.py](../OriginalModel/prob.py) except for the acceptance probability
    computation where it takes the outdegree of the node.

-   `rumour_spread_model.py`: This file almost same as 
    [OriginalModel/rumour_spread_model.py](../OriginalModel/rumour_spread_model.py). It does 
    the same function but some implementations have been changed to incorporate the directed graph
    model. It's description can be found at 
    [OriginalModel/README.md](../OriginalModel/README.md).

-   `callbacks.py`: This file is almost same as [OriginalModel/callbacks.py](../OriginalModel/callbacks.py), 
    and it is described in [OriginalModel/README.md](../DirectedGraph/README.md). There is a
    small change in the file because of the directed graph model. 

-   `plot.py`: This file is same as [OriginalModel/plot.py](../OriginalModel/plot.py), 
    and the description can be found here: [OriginalModel/README.md](../OriginalModel/README.md).
    
-   `simulate.py` : This file is same as [OriginalModel/simulate.py](../OriginalModel/simulate.py)
    but with some extra parameters used to generate directed scale-free graph. The description
    is at [OriginalModel/README.md](../OriginalModel/README.md).
    
-   `simulate_with_adversary.py` : This file similar to the above the file but it also introduces
    adversary and finally generates the plots. This was also used to get the results which we wrote 
    in the paper.
    
-   `simulate_single.py` : This file takes conservation factor, confidence factor and number of
    adversary nodes as arguments and produces the `RangeOfInformationSpread`, 
    `OpinionFragmentation` and `Average Information Entropy` plots. This file is same as
    [OriginalModel/simulate_single.py](../OriginalModel/simulate_single.py) and 
    the description is in [OriginalModel/README.md](../OriginalModel/README.md).


Observation: The file descriptions given in this markdown are presented in a
topological order of the dependency graph of these files.

# Faster Directed Graph Experimental

This directory contains the codes for the simulation of the directed graph version (described in our paper [rumour_spread](../rumour_spread.pdf)) of the original undirected graph model ([original model](https://www.nature.com/articles/s41598-017-09171-8)). It does the same simulation as the 
[DirectedGraph/](../DirectedGraph/) codes. The only difference is the the data structure used to implement the memory of the nodes.

## Files Description

-   `graph.py`: Same as 
    [DirectedGraph/graph.py](../DirectedGraph/graph.py), and described in 
    [DirectedGraph/README.md](../DirectedGraph/README.md)

-   `scale_free.py`: The file is same as 
    [DirectedGraph/scale_free.py](../DirectedGraph/scale_free.py), and described in 
    [DirectedGraph/README.md](../DirectedGraph/README.md)

-   `memory_queue.py`: It implements the memory queue data structure same as in 
    [OriginalModel/memory_queue.py](../OriginalModel/memory_queue.py) but instead of using queue
    data structure and maps, it uses multiple 
    [sortedcontainers](https://pypi.org/project/sortedcontainers/0.8.4/)
    and time counter. The queue data structure would take O(1) time in enqueue and dequeue
    operations but O(n) time to modify (or deletion + insertion) at any position (here, n
     is the length of the queue). Since we need to enqueue, dequeue and distort information at 
     some places, it is not efficient for memory queue having large capacity.
     
     Since [SortedList](http://www.grantjenks.com/docs/sortedcontainers/sortedlist.html) can perform insertion, 
     deletion at any location in O(logn) where n 
     is the size of the SortedList and it can store the values in sorted order, we can use it
     multiple of it to implement the same memory queue but with O(logn) time complexity for 
     each of the required operations.

-   `prob.py`: The file is same as 
    [DirectedGraph/prob.py](../DirectedGraph/prob.py), and described in 
    [DirectedGraph/README.md](../DirectedGraph/README.md)

-   `rumour_spread_model.py`: This file is almost same as 
    [DirectedGraph/rumour_spread_model.py](../DirectedGraph/rumour_spread_model.py). It does 
    the same function but some implementations have been changed because of the new data structure
    of the memory queue. It's description can be found at 
    [DirectedGraph/README.md](../DirectedGraph/README.md).

-   `callbacks.py`: This file is almost same as [DirectedGraph/callbacks.py](../DirectedGraph/callbacks.py), 
    and it is described in [DirectedGraph/README.md](../DirectedGraph/README.md). There is a
    small change in the file because of the new memory queue data structure. 

-   `plot.py`: This file is same as [OriginalModel/plot.py](../OriginalModel/plot.py), 
    and the description can be found here: [OriginalModel/README.md](../OriginalModel/README.md).

-   `simulate.py` : The file is same as 
    [DirectedGraph/simulate.py](../DirectedGraph/simulate.py), and described in 
    [DirectedGraph/README.md](../DirectedGraph/README.md)
    
-   `simulate_with_adversary.py` : The file is same as 
    [DirectedGraph/simulate_with_adversary.py](../DirectedGraph/simulate_with_adversary.py), 
    and described in [DirectedGraph/README.md](../DirectedGraph/README.md)

Observation: The file descriptions given in this markdown are presented in a
topological order of the dependency graph of these files.

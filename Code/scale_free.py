import random

from graph import Graph

def generate_spanning_tree(n):
    
    spanning_tree = Graph(n)

    for i in range(1, n):
        j = random.randint(0, i - 1)
        spanning_tree.add_edge(i, j)

    return spanning_tree

def generate_scale_free(n, init_num_nodes, num_edges_per_step):
    pass

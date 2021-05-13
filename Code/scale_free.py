import numpy as np

from graph import Graph

def initialize_graph(n, init_num_nodes):
    
    spanning_tree = Graph(n)

    for i in range(1, init_num_nodes):
        j = np.random.randint(0, i)
        spanning_tree.add_edge(i, j)

    return spanning_tree

def generate_scale_free(n, init_num_nodes, num_edges_per_step):
    
    graph = initialize_graph(n, init_num_nodes)

    deg_list = np.zeros(n, dtype=np.int32)
    deg_list[:init_num_nodes] = 1

    for i in range(init_num_nodes, n):
        deg_prob = deg_list[:i].astype(np.float32)
        deg_prob /= deg_prob.sum()

        verts = np.random.choice(i, num_edges_per_step, False, deg_prob)

        for j in verts:
            graph.add_edge(i, j)
            deg_list[j] += 1

        deg_list[i] += num_edges_per_step

    return graph

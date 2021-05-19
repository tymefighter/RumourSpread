import numpy as np

from graph import Graph

def initialize_graph(n, init_num_nodes):
    
    tree = Graph(n)
    indeg = np.zeros(n)
    outdeg = np.zeros(n)

    for i in range(1, init_num_nodes):
        j = np.random.randint(0, i)
        tree.add_edge(j, i)

        outdeg[j] += 1
        indeg[i] += 1

    return tree, indeg, outdeg

def generate_scale_free(
    n, init_num_nodes,
    alpha, beta, gamma,
    delta_in, delta_out
):
    
    graph, indeg, outdeg = initialize_graph(n, init_num_nodes)
    i = init_num_nodes

    num_edges = np.sum(indeg)
    while i < n:

        choice = np.random.choice(
            ['to-vert', 'btw-vert', 'from-vert'],
            p=[alpha, beta, gamma]
        )

        if choice == 'to-vert':
            v = np.random.choice(
                i, p=(indeg[:i] + delta_in) / (num_edges + i * delta_in)
            )
            graph.add_edge(i, v)
            outdeg[i] += 1
            indeg[v] += 1
            i += 1

        elif choice == 'btw-vert':
            u = np.random.choice(
                i, p=(outdeg[:i] + delta_out) / (num_edges + i * delta_out)
            )
            v = np.random.choice(
                i, p=(indeg[:i] + delta_in) / (num_edges + i * delta_in)
            )
            graph.add_edge(u, v)
            outdeg[u] += 1
            indeg[v] += 1

        else:
            u = np.random.choice(
                i, p=(outdeg[:i] + delta_out) / (num_edges + i * delta_out)
            )
            graph.add_edge(u, i)
            outdeg[u] += 1
            indeg[i] += 1
            i += 1

        num_edges += 1

    return graph

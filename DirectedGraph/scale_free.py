import numpy as np

from graph import Graph

def initialize_graph_tree(n, init_num_nodes):
    
    tree = Graph(n)
    indeg = np.zeros(n)
    outdeg = np.zeros(n)
    edge_set = set()

    for i in range(1, init_num_nodes):
        j = np.random.randint(0, i)
        tree.add_edge(j, i)

        outdeg[j] += 1
        indeg[i] += 1

        edge_set.add((i, j))

    return tree, indeg, outdeg, edge_set

def generate_scale_free(
    n, init_num_nodes,
    alpha, beta, gamma,
    delta_in, delta_out
):
    
    graph, indeg, outdeg, edge_set = initialize_graph_tree(n, init_num_nodes)
    i = init_num_nodes

    num_edges = len(edge_set)
    while i < n:

        choice = np.random.choice(
            ['to-vert', 'btw-vert', 'from-vert'],
            p=[alpha, beta, gamma]
        )

        if choice == 'to-vert':
            u = i
            v = np.random.choice(
                i, p=(indeg[:i] + delta_in) / (num_edges + i * delta_in)
            )
            i += 1

        elif choice == 'btw-vert':

            already_present = True
            while already_present:
                u = np.random.choice(
                    i, p=(outdeg[:i] + delta_out) / (num_edges + i * delta_out)
                )
                v = np.random.choice(
                    i, p=(indeg[:i] + delta_in) / (num_edges + i * delta_in)
                )

                already_present = (u, v) in edge_set

        else:
            u = np.random.choice(
                i, p=(outdeg[:i] + delta_out) / (num_edges + i * delta_out)
            )
            v = i
            i += 1

        graph.add_edge(u, v)
        edge_set.add((u, v))
        outdeg[u] += 1
        indeg[v] += 1
        num_edges += 1

    return graph

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

def make_strongly_conncted(graph, delta_in, delta_out):

    scc = graph.scc()
    outdeg = np.array(graph.compute_outdegrees())
    indeg = np.array(graph.compute_indegrees())

    while len(scc) > 1:
        i, j = np.random.choice(len(scc), size=2, replace=False)

        comp1, comp2 = np.array(scc[i]), np.array(scc[j])

        u = np.random.choice(
            comp1, 
            p=(outdeg[comp1] + delta_out) \
                / (np.sum(outdeg[comp1]) + comp1.size * delta_out)
        )
        v = np.random.choice(
            comp2, 
            p=(indeg[comp2] + delta_out) \
                / (np.sum(indeg[comp2]) + comp2.size * delta_out)
        )
        graph.add_edge(u, v)

        u = np.random.choice(
            comp2, 
            p=(outdeg[comp2] + delta_out) \
                / (np.sum(outdeg[comp2]) + comp2.size * delta_out)
        )
        v = np.random.choice(
            comp1, 
            p=(indeg[comp1] + delta_out) \
                / (np.sum(indeg[comp1]) + comp1.size * delta_out)
        )
        graph.add_edge(u, v)

        scc[i].extend(scc[j])
        scc.pop(j)

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

    make_strongly_conncted(graph, delta_in, delta_out)

    return graph

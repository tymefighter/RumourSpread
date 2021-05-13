class Graph:

    def __init__(self, n):

        self.n = n
        self.adj_list = [[] for i in range(n)]

    def add_edge(self, u, v):

        self.adj_list[u].append(v)

    def compute_degrees(self):

        return [len(self.adj_list[i]) for i in range(self.n)]

    def compute_degree_distribution(self):

        deg_list = self.compute_degrees()

        n = len(deg_list)
        deg_dist = [0] * n

        for deg in deg_list:
            deg_dist[deg] += 1

        return deg_dist

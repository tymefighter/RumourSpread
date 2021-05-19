import numpy as np

class Graph:

    def __init__(self, n):

        self.n = n
        self.adj_list = [[] for i in range(n)]

    def add_edge(self, u, v):

        self.adj_list[u].append(v)

    def add_node(self):

        self.n += 1
        self.adj_list.append([])

        return self.n - 1

    def compute_indegrees(self):

        indeg_list = [0] * self.n

        for node in range(self.n):
            for out_nbr in self.adj_list[node]:
                indeg_list[out_nbr] += 1
            
        return indeg_list
    
    def compute_outdegrees(self):

        return [len(self.adj_list[i]) for i in range(self.n)]

    def compute_indegree_distribution(self):

        indeg_list = self.compute_indegrees()
        indeg_dist = [0] * self.n

        for deg in indeg_list:
            indeg_dist[deg] += 1

        return indeg_dist
    
    def compute_outdegree_distribution(self):

        outdeg_list = self.compute_outdegrees()
        outdeg_dist = [0] * self.n

        for deg in outdeg_list:
            outdeg_dist[deg] += 1

        return outdeg_dist

    def compute_diameter(self):

        dp = np.full((self.n, self.n), np.inf)

        for node in range(self.n):
            for nbr in self.adj_list[node]:
                dp[node, nbr] = 1

        for k in range(self.n):
            dp = np.minimum(
                dp, np.expand_dims(dp[:, k], axis=1) 
                + np.expand_dims(dp[k, :], axis=0))

        diameter = np.max(dp)

        return 'infinity' if diameter == np.inf else diameter

import numpy as np
from collections import deque

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

    def compute_diameter(self, check_inf=False):

        dp = np.full((self.n, self.n), np.inf)

        for node in range(self.n):
            for nbr in self.adj_list[node]:
                dp[node, nbr] = 1

        for k in range(self.n):
            dp = np.minimum(
                dp, np.expand_dims(dp[:, k], axis=1) 
                + np.expand_dims(dp[k, :], axis=0))

        diameter = np.max(dp) if not check_inf else np.max(dp[dp != np.inf])

        return 'infinity' if diameter == np.inf else diameter

    def dfs_rev(self, adj_rev, u, visited, dq):
        visited[u] = True

        for v in adj_rev[u]:
            if not visited[v]:
                self.dfs_rev(adj_rev, v, visited, dq)

        dq.appendleft(u)

    def dfs(self, u, visited, comp):
        visited[u] = True
        comp.append(u)

        for v in self.adj_list[u]:
            if not visited[v]:
                self.dfs(v, visited, comp)

    def scc(self):

        adj_rev = [[] for _ in range(self.n)]

        for node in range(self.n):
            for nbr in self.adj_list[node]:
                adj_rev[nbr].append(node)

        dq = deque()
        visited = [False for _ in range(self.n)]

        for u in range(self.n):
            if not visited[u]:
                self.dfs_rev(adj_rev, u, visited, dq)

        visited = [False for _ in range(self.n)]
        comp_list = []
        for u in list(dq):
            if not visited[u]:
                comp = []
                comp_list.append(comp)
                self.dfs(u, visited, comp)

        return comp_list

    def get_edge_list(self):

        edge_list = []
        for node in range(self.n):
            for nbr in self.adj_list[node]:
                edge_list.append((node, nbr))

        return edge_list

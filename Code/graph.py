class Graph:

    def __init__(self, n):

        self.adj_list = [[] for i in range(n)]

    def add_edge(self, u, v):

        self.adj_list[u].append(v)

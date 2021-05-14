from random import randint, choices

from memory_queue import MemoryQueue
from prob import Prob
from scale_free import generate_scale_free

class RumourSpreadModel:

    def __init__(
        self, num_nodes, num_bits, node_capacity, conservation_factor,
        confidence_factor, init_num_nodes=1, num_edges_per_step=1
    ):
        self.num_nodes = num_nodes
        self.num_bits = num_bits
        self.prob = Prob(num_bits, conservation_factor, confidence_factor)
        self.scale_free_graph = generate_scale_free(
            num_nodes, init_num_nodes, num_edges_per_step
        )
        self.nodes_memory = [
            MemoryQueue(node_capacity) for _ in range(num_nodes)
        ]

    def distort_info(self, x):

        bit_pos = randint(0, self.num_bits - 1)
        return (x ^ (1 << bit_pos))
    
    def get_distorted_info(self):

        distorted_info = []
        for node_memory in self.nodes_memory:

            if len(node_memory.deque) <= 0:
                distorted_info.append(None)
                continue

            most_freq_info = node_memory.get_most_freq_elem()
            distortion_prob = self.prob.compute_distortion_prob(
                node_memory.compute_entropy()
            )

            if choices(
                    population=[True, False],
                    weights=[distortion_prob, 1 - distortion_prob],
                    k=1
            )[0] == True:
                distorted_info.append(distort_info(most_freq_info))
            else:
                distorted_info.append(most_freq_info)

        return distorted_info

    def update_node_memory(self, buffer_info):

        nodes_degree = self.scale_free_graph.compute_degree()

        # acceptance at 'node'
        for node in range(self.num_nodes):

            adj_list = self.scale_free_graph.adj_list[node]
            max_nbr_degree = 0
            degree = nodes_degree[node]

            for nbr in adj_list:
                max_nbr_degree = max(max_nbr_degree, nodes_degree[nbr])

            for nbr in adj_list:
                if buffer_memory[nbr] is None:
                    continue
                
                # acctance prob of 'node' from 'nbr'
                acceptance_prob = self.prob.compute_acceptance_prob(
                    degree, max_nbr_degree
                )

                if choices(
                    population=[True, False],
                    weights=[acceptance_prob, 1 - acceptance_prob],
                    k=1
            )[0] == True:
                self.nodes_memory[node].insert(buffer_info[node])

                
    def simulate_step(self):
        
        
    def simulate(self, time_steps):

        for t in range(time_steps):
            self.simulate_step()

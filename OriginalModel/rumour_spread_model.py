from random import randint, random

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
            MemoryQueue(num_bits, node_capacity) for _ in range(num_nodes)
        ]

    def get_graph(self):

        return self.scale_free_graph

    def get_nodes_memory(self):

        return self.nodes_memory

    def distort_info(self, x):

        bit_pos = randint(0, self.num_bits - 1)
        return (x ^ (1 << bit_pos))
    
    def get_distorted_info(self):

        distorted_info = []
        for node_memory in self.nodes_memory:

            if node_memory.is_empty():
                distorted_info.append(None)
                continue

            most_freq_info = node_memory.get_most_freq_elem()
            distortion_prob = self.prob.compute_distortion_prob(
                node_memory.compute_entropy()
            )

            if random() <= distortion_prob:
                dist_info = self.distort_info(most_freq_info)
                node_memory.distort_in_memory(most_freq_info, dist_info)
                distorted_info.append(dist_info)
            else:
                distorted_info.append(most_freq_info)

        return distorted_info

    def update_node_memory(self, buffer_info):

        nodes_degree = self.scale_free_graph.compute_degrees()

        for node in range(self.num_nodes):

            nbr_list = self.scale_free_graph.adj_list[node]
            max_nbr_degree = 0
            min_nbr_degree = self.num_nodes
            degree = nodes_degree[node]

            for nbr in nbr_list:
                max_nbr_degree = max(max_nbr_degree, nodes_degree[nbr])
                min_nbr_degree = min(min_nbr_degree, nodes_degree[nbr])

            for nbr in nbr_list:
                if buffer_info[nbr] is None:
                    continue
                
                acceptance_prob = self.prob.compute_acceptance_prob(
                    degree, max_nbr_degree, min_nbr_degree
                )

                if random() <= acceptance_prob:
                    self.nodes_memory[node].insert(buffer_info[nbr])

    def inject_info(self, info_propagators):

        for node, info in info_propagators.items():
            self.nodes_memory[node].insert(info)
                
    def simulate_step(self):

        distorted_info = self.get_distorted_info()
        self.update_node_memory(distorted_info)
        
    def simulate(self, info_propagators, time_steps, callback_list):

        self.inject_info(info_propagators)
        for t in range(time_steps):
            self.simulate_step()

            for callback in callback_list:
                callback.call_after_step(self, t)

        return [callback.get_result() for callback in callback_list]

class Callback:

    def __init__(self):
        pass

    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):
        pass

    def get_result(self):
        pass

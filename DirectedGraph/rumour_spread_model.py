from random import randint, random

from memory_queue import MemoryQueue
from prob import Prob
from scale_free import generate_scale_free
from plot import plot_degree_distribution

class RumourSpreadModel:

    def __init__(
        self, num_nodes, num_bits, node_capacity, 
        conservation_factor, confidence_factor,
        init_num_nodes, alpha, beta, gamma, delta_in, delta_out,
        plot_degree_dist=False
    ):
        self.num_nodes = num_nodes
        self.num_bits = num_bits
        self.prob = Prob(num_bits, conservation_factor, confidence_factor)
        self.scale_free_graph = generate_scale_free(
            num_nodes, init_num_nodes,
            alpha, beta, gamma,
            delta_in, delta_out
        )
        self.nodes_memory = [
            MemoryQueue(num_bits, node_capacity) for _ in range(num_nodes)
        ]

        if plot_degree_dist:
            plot_degree_distribution(
                self.scale_free_graph.compute_outdegree_distribution(), 
                int(0.08 * num_nodes),
                'Outdegree Distribution'
            )

            plot_degree_distribution(
                self.scale_free_graph.compute_indegree_distribution(), 
                int(0.08 * num_nodes),
                'Indegree Distribution'
            )

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

        nodes_outdegree = self.scale_free_graph.compute_outdegrees()
        max_nbr_outdegree = [0] * self.num_nodes
        min_nbr_outdegree = [self.num_nodes] * self.num_nodes
        
        for node in range(self.num_nodes):
            nbr_list = self.scale_free_graph.adj_list[node]
            degree = nodes_outdegree[node]

            for nbr in nbr_list:
                max_nbr_outdegree[nbr] = max(max_nbr_outdegree[nbr], degree)
                min_nbr_outdegree[nbr] = min(min_nbr_outdegree[nbr], degree)

        for node in range(self.num_nodes):

            if buffer_info[node] is None:
                continue
            
            nbr_list = self.scale_free_graph.adj_list[node]
            degree = nodes_outdegree[node]
            
            for nbr in nbr_list:
                acceptance_prob = self.prob.compute_acceptance_prob(
                    degree, max_nbr_outdegree[nbr], min_nbr_outdegree[nbr]
                )

                if random() <= acceptance_prob:
                    self.nodes_memory[nbr].insert(buffer_info[node])

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

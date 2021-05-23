from random import randint, random
from math import log2
from memory_queue import MemoryQueue
from prob import Prob
from scale_free import generate_scale_free

class RumourSpreadModel:

    def __init__(
        self, num_nodes, num_bits, node_capacity, 
        conservation_factor, confidence_factor,
        init_num_nodes, alpha, beta, gamma, delta_in, delta_out
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
            MemoryQueue(node_capacity) for _ in range(num_nodes)
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
                    info = buffer_info[node]
                    self.nodes_memory[nbr].insert(info)
                
                else:
                    info = -1

                if self.edge_info_freq is not None:
                    edge = (node, nbr)
                    if info not in self.edge_info_freq[edge]:
                        self.edge_info_freq[edge][info] = 1
                    else:
                        self.edge_info_freq[edge][info] += 1

    def inject_info(self, info_propagators):

        for node, info in info_propagators.items():
            self.nodes_memory[node].insert(info)
                
    def simulate_step(self):

        distorted_info = self.get_distorted_info()
        self.update_node_memory(distorted_info)

    def compute_entropy(self, val_freq):
        entropy = 0.0
        total_sum = sum(val_freq.values())

        for freq in val_freq.values():
            prob = freq / total_sum
            entropy -= prob * log2(prob)

        return entropy
        
    def simulate(self, info_propagators, time_steps, callback_list,
        node_info_timestep_list, edge_info_timerange_list):

        node_info_timestep_list.reverse()
        edge_info_timerange_list.reverse()

        node_entropy_list = []
        edge_entropy_list = []
        self.edge_info_freq = None

        self.inject_info(info_propagators)
        for t in range(time_steps):
            if len(node_info_timestep_list) > 0 \
                and node_info_timestep_list[-1] == t:

                node_entropies = []
                for node_memory in self.nodes_memory:
                    node_entropies.append(node_memory.compute_entropy())

                node_entropy_list.append(node_entropies)
                node_info_timestep_list.pop()

            self.t = t
            if len(edge_info_timerange_list) > 0:
                if edge_info_timerange_list[-1][0] == t:

                    self.edge_info_freq = dict()
                    for edge in self.scale_free_graph.get_edge_list():
                        self.edge_info_freq[edge] = dict()

                    self.t_start, self.t_end = edge_info_timerange_list[-1]

                elif edge_info_timerange_list[-1][1] == t:

                    edge_entropies = []
                    for val_freq in self.edge_info_freq.values():
                        edge_entropies.append(self.compute_entropy(val_freq))

                    edge_entropy_list.append(edge_entropies)
                    edge_info_timerange_list.pop()

                    self.edge_info_freq = None

            self.simulate_step()

            for callback in callback_list:
                callback.call_after_step(self, t)
    
        return [callback.get_result() for callback in callback_list], \
            node_entropy_list, edge_entropy_list

class Callback:

    def __init__(self):
        pass

    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):
        pass

    def get_result(self):
        pass

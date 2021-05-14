from random import randint, choices

from memory_queue import MemoryQueue
from prob import Prob
from scale_free import generate_scale_free

class RumourSpreadModel:

    def __init__(
        self, num_nodes, num_bits, node_capacity, conservation_factor,
        confidence_factor, init_num_nodes=1, num_edges_per_step=1
    ):
        self.prob = Prob(num_bits, conservation_factor, confidence_factor)
        self.scale_free_graph = generate_scale_free(
            num_nodes, init_num_nodes, num_edges_per_step
        )
        self.nodes_memory = [
            MemoryQueue(node_capacity) for _ in range(num_nodes)
        ]

    def distort_info(self, x):

        bit_pos = randint(0, num_bits - 1)
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
            
    def simulate_step(self):
        
        
    def simulate(self, time_steps):

        for t in range(time_steps):
            self.simulate_step()

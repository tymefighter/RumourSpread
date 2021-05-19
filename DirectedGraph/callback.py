from rumour_spread_model import RumourSpreadModel, Callback

class RangeOfInformationSpread(Callback):

    def __init__(self, num_nodes, num_bits, time_steps):
        super().__init__()

        num_values = 1 << num_bits
        self.bit_counts = [[0] * num_values for _ in range(time_steps)]
        self.num_nodes = num_nodes

    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):
        
        bit_count_list = self.bit_counts[t]

        for node_memory in rumour_spread.get_nodes_memory():
            for x in node_memory.get_freq_dict().keys():
                bit_count_list[x] += 1

    def get_result(self):

        for bit_count_list in self.bit_counts:
            for i in range(len(bit_count_list)):
                bit_count_list[i] /= self.num_nodes

        return self.bit_counts

class OpinionFragmentation(Callback):

    def __init__(self, num_nodes, num_bits, time_steps):
        super().__init__()

        num_values = 1 << num_bits
        self.opinion_freq = [[0] * num_values for _ in range(time_steps)]
        self.num_nodes = num_nodes
        
    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):

        opinion_freq_list = self.opinion_freq[t]
        
        for node_memory in rumour_spread.get_nodes_memory():
            for freq_elem in node_memory.get_most_freq_elem(get_all=True):
                opinion_freq_list[freq_elem] += 1
        
    def get_result(self):
                
        for opinion_freq_list in self.opinion_freq:
            for i in range(len(opinion_freq_list)):
                opinion_freq_list[i] /= self.num_nodes

        return self.opinion_freq

class AverageInformationEntropy(Callback):

    def __init__(self, num_nodes, time_steps):
        super().__init__()

        self.avg_entropy = [0.0] * time_steps
        self.num_nodes = num_nodes
        
    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):
        
        for node_memory in rumour_spread.get_nodes_memory():
            self.avg_entropy[t] += node_memory.compute_entropy()

        self.avg_entropy[t] /= self.num_nodes
        
    def get_result(self):

        return self.avg_entropy

class Adversary(Callback):

    def __init__(self, feed_value, num_target_nodes, start_timestep):
        super().__init__()

        self.feed_value = feed_value
        self.num_target_nodes = num_target_nodes
        self.start_timestep = start_timestep
        self.first_run = True

    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):

        if t < self.start_timestep:
            return

        if self.first_run:

            outdeg_list = rumour_spread.get_graph().compute_outdegrees()
            outdeg_idx_list = [(outdeg_list, i) for i in range(len(outdeg_list))]

            sorted(outdeg_idx_list, key=lambda x: x[0], reverse=True)

            target_nodes = [
                outdeg_idx_list[i][1] for i in range(self.num_target_nodes)
            ]

            nodes_memory = rumour_spread.get_nodes_memory()

            class FixedMemory:

                def __init__(self, feed_value):
                    self.feed_value = feed_value

                def insert(self, x):
                    pass

                def insert_list(self, lst):
                    pass

                def get_most_freq_elem(self):
                    return self.feed_value

                def compute_entropy(self):
                    return 0

                def is_empty(self):
                    return False

                def get_freq_dict(self):
                    return {self.feed_value: 1}

            for node in target_nodes:
                nodes_memory[node] = FixedMemory(self.feed_value)

            self.first_run = False

    def get_result(self):
        return None

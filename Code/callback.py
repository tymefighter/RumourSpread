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
        self.bit_counts = [[0] * num_values for _ in range(time_steps)]
        self.num_nodes = num_nodes
        
    def call_after_step(self, rumour_spread: RumourSpreadModel, t: int):

        for node_memory in rumour_spread.nodes_memory():
            if len(node_memory.deque) > 0:
                self.bit_counts[node_memory.get_most_freq_elem()] += 1
        
    def get_result(self):
                
        for bit_count_list in self.bit_counts:
            for i in range(len(bit_count_list)):
                bit_count_list[i] /= self.num_nodes

        return self.bit_counts

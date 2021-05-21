from sortedcontainers import SortedList
from random import choice
from math import log2

INFINITY = int(1e18)

class MemoryQueue:

    def __init__(self, num_bits, capacity):

        self.num_bits = num_bits
        self.capacity = capacity
        self.size = 0
        self.time = 0
        self.bit_lists = [SortedList() for _ in range(1 << num_bits)]
        self.freq_dict = dict()

    def __len__(self):

        return self.size

    def is_empty(self):

        return self.size == 0

    def get_freq_dict(self):

        return self.freq_dict


    def insert(self, x):
        
        if self.size == self.capacity:

            oldest_time = INFINITY
            oldest_val = None
            
            for k in self.freq_dict.keys():
                
                time_t =  self.bit_lists[k][0]        
                if time_t < oldest_time:
                    oldest_time = time_t
                    oldest_val = k

            if oldest_val is not None:

                del self.bit_lists[oldest_val][0]
                self.freq_dict[oldest_val] -= 1
                if self.freq_dict[oldest_val] == 0:
                    del self.freq_dict[oldest_val]

                self.size -= 1

        self.bit_lists[x].add(self.time)
        if x not in self.freq_dict:
            self.freq_dict[x] = 1
        else:
            self.freq_dict[x] += 1

        self.time += 1
        self.size += 1

    def insert_list(self, lst):

        for x in lst:
            self.insert(x)
    
    def get_most_freq_elem(self, get_all=False):

        max_freq = 0
        for _, freq in self.freq_dict.items():
            max_freq = max(max_freq, freq)

        most_freq_elem_list = []
        for bit in range(1 << self.num_bits):
            if len(self.bit_lists[bit]) == max_freq:
                most_freq_elem_list.append(bit)

        ret_val = most_freq_elem_list
        if not get_all:
            ret_val = choice(ret_val) 

        return ret_val

    def compute_entropy(self):

        entropy = 0.0

        for _, freq in self.freq_dict.items():

            prob = freq / self.size
            entropy += prob * log2(prob)

        return -entropy

    def distort_in_memory(self, old_info, new_info):

        first_occ_t = self.bit_lists[old_info][0]

        del self.bit_lists[old_info][0]
        self.bit_lists[new_info].add(first_occ_t)

        self.freq_dict[old_info] -= 1
        if self.freq_dict[old_info] == 0:
            del self.freq_dict[old_info]
                    
        if new_info not in self.freq_dict:
            self.freq_dict[new_info] = 1
        else:
            self.freq_dict[new_info] += 1

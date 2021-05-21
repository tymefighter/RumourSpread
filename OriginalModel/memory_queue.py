from sortedcontainers import SortedList
from random import choice
from math import log2

class MemoryQueue:

    def __init__(self, num_bits, capacity):

        self.num_bits = num_bits
        self.capacity = capacity
        self.size = 0
        self.time = 0
        self.bit_lists = [SortedList() for _ in range(1 << num_bits)]
        self.freq_list = SortedList()
        self.time_list = SortedList()

    def __len__(self):

        return self.size

    def is_empty(self):

        return self.size == 0

    def get_freq_list(self):

        return list(self.freq_list)


    def insert(self, x):
        
        if self.size == self.capacity:

            time, val = self.time_list[0]

            del self.time_list[0]
            self.freq_list.remove((len(self.bit_lists[val]), val))
            del self.bit_lists[val][0]
            
            if len(self.bit_lists[val]) > 0:
                self.freq_list.add(len(self.bit_lists[val]), val)

            self.size -= 1

        if len(self.bit_lists[x]) > 0:
            self.freq_list.remove((len(self.bit_lists[x]), x))
        
        self.bit_lists[x].add(self.time)
        self.time_list.add((self.time, x))
        self.freq_list.add((len(self.bit_lists[x]), x))

        self.time += 1
        self.size += 1

    def insert_list(self, lst):

        for x in lst:
            self.insert(x)
    
    def get_most_freq_elem(self, get_all=False):

        max_freq = self.freq_list[-1][0]
        most_freq_elem_list = []
        
        for i in range(0, len(self.freq_list)):

            freq_pair = self.freq_list[-i - 1]
            if freq_pair[0] == max_freq:
                most_freq_elem_list.append(freq_pair[1])
            else:
                break

        ret_val = most_freq_elem_list
        if not get_all:
            ret_val = choice(ret_val) 

        return ret_val

    def compute_entropy(self):

        entropy = 0.0

        for freq, _ in list(self.freq_list):

            prob = freq / self.size
            entropy += prob * log2(prob)

        return -entropy

    def distort_in_memory(self, old_info, new_info):

        time_old = self.bit_lists[old_info][0]
        freq_old = len(self.bit_lists[old_info])
        freq_new = len(self.bit_lists[new_info])


        del self.bit_lists[old_info][0]
        self.bit_lists[new_info].add(time_old)

        self.freq_list.remove((freq_old, old_info))
        self.freq_list.remove((freq_new, new_info))

        freq_old -= 1
        freq_new += 1
        
        if freq_old > 0:
            self.freq_list.add((freq_old, old_info))

        self.freq_list.add((freq_new, new_info))

        self.time_list.remove((time_old, old_info))
        self.time_list.add((time_old, new_info))

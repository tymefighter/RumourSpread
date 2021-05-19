from queue_ref import Queue
from random import choice
from math import log2

class MemoryQueue:

    def __init__(self, capacity):
        
        self.queue = Queue()
        self.capacity = capacity
        self.size = 0
        self.freq_dict = dict()

    def __len__(self):

        return self.size

    def is_empty(self):

        return self.size == 0

    def get_freq_dict(self):

        return self.freq_dict

    def insert(self, x):

        if self.size == self.capacity:
            y = self.queue.dequeue()

            self.freq_dict[y] -= 1
            if self.freq_dict[y] == 0:
                del self.freq_dict[y]

            self.size -= 1

        if x not in self.freq_dict:
            self.freq_dict[x] = 1
        else:
            self.freq_dict[x] += 1

        self.queue.enqueue(x)
        self.size += 1

    def insert_list(self, lst):

        for x in lst:
            self.insert(x)
    
    def get_most_freq_elem(self, get_all=False):

        max_freq = 0
        for freq in self.freq_dict.values():
            max_freq = max(max_freq, freq)

        most_freq_elem_list = []
        for x, freq in self.freq_dict.items():
            if freq == max_freq:
                most_freq_elem_list.append(x)

        ret_val = most_freq_elem_list
        if not get_all:
            ret_val = choice(ret_val) 

        return ret_val

    def compute_entropy(self):

        entropy = 0.0

        for freq in self.freq_dict.values():

            prob = freq / self.size
            entropy += prob * log2(prob)

        return -entropy

    def distort_in_memory(self, old_info, new_info):

        self.queue.update_first_occ(old_info, new_info)
        self.freq_dict[old_info] -= 1

        if self.freq_dict[old_info] == 0:
            del self.freq_dict[old_info]

        if new_info not in self.freq_dict:
            self.freq_dict[new_info] = 1
        else:
            self.freq_dict[new_info] += 1

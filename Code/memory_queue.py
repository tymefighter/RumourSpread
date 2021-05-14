from collections import deque
from random import choice
from math import log2

class MemoryQueue:

    def __init__(self, capacity):
        
        self.deque = deque()
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
            y = self.deque.popleft()

            self.freq_dict[y] -= 1
            if self.freq_dict[y] == 0:
                del self.freq_dict[y]

            self.size -= 1

        if x not in self.freq_dict:
            self.freq_dict[x] = 1
        else:
            self.freq_dict[x] += 1

        self.deque.append(x)
        self.size += 1

    def insert_list(self, lst):

        for x in lst:
            self.insert(x)
    
    def get_most_freq_elem(self):

        max_freq = 0
        for freq in self.freq_dict.values():
            max_freq = max(max_freq, freq)

        most_freq_elem_list = []
        for x, freq in self.freq_dict.items():
            if freq == max_freq:
                most_freq_elem_list.append(x)

        return choice(most_freq_elem_list)

    def compute_entropy(self):

        entropy = 0.0

        for freq in self.freq_dict.values():

            prob = freq / self.size
            entropy += prob * log2(prob)

        return -entropy

class QueueNode:

    def __init__(self, val):
        self.val = val
        self.next = None

class Queue:

    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def enqueue(self, val):

        if self.head is None:
            self.head = self.tail = QueueNode(val)

        else:
            self.tail.next = QueueNode(val)
            self.tail = self.tail.next

        self.size += 1

    def dequeue(self):

        assert self.head is not None

        deq_value = self.head.val
        self.head = self.head.next

        if self.head is None:
            self.tail = self.head

        self.size -= 1

        return deq_value

    def update_first_occ(self, old_value, new_value):

        node = self.head 

        while node is not None and node.val != old_value:
            node = node.next

        if node is not None:
            node.val = new_value

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.head is None

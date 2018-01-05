class Node:
    def __init__(self, cargo):
        self.cargo = cargo
        self.next = None

    def __iter__(self):
        for i in range(1):
            yield self.cargo

    def __str__(self):
        return str(self.cargo)

class Fila:
    '''
    Assumes the elements pushed are non-iterable.
    '''
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.cargo
            current = current.next

    def __str__(self):
        string = []
        for element in self:
            string.append(str(element))
        return ', '.join(string)

    __repr__ = __str__

    def __len__(self):
         return self.length

    def clear(self):
        self.length = 0
        self.head = None
        self.tail = None

    def push(self, valor):
        node = Node(valor)
        if self.length == 0:
            self.head = self.tail = node
        else:
            temp = self.tail
            temp.next = node
            self.tail = node
        self.length += 1

    def pop(self):
        if self.length == 0:
            return None
        else:
            temp = self.head
            self.head = self.head.next
            self.length -= 1
            return temp.cargo

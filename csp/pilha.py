class Pilha:
    '''
    __str__ method assumes elements are not strings and can be converted to string.
    Assumes objects being pushed are iterables.
    '''

    def __init__(self):
        self.lista = []
        self.top = None

    def __iter__(self):
        for i in self.lista:
            yield i

    def __len__(self):
         return len(self.lista)

    def __str__(self):
        string = []
        for index in range(len(self.lista)-1, -1, -1):
            string.append(str(self.lista[index]))
        return ', '.join(string)

    __repr__ = __str__

    def clear(self):
        self.lista = []

    def push(self, new):
        '''Recieves a non-iterable object'''
        self.lista.append(new)
        self.top = self.lista[-1]

    def extend(self, new):
        '''Recieves an iterable object'''
        self.lista.extend(new)
        if self.lista:
            self.top = self.lista[-1]

    def pop(self):
        if not self.lista:
            return None
        dado = self.lista[-1]
        del self.lista[-1]
        return dado

if __name__ == '__main__':
    a = Pilha()
    a.push([1])
    a.push([2])
    a.push([3])
    a.push([])

    b = Pilha()
    b.push(a)

    for element in a:
        print('Hi!')

    print(a)
    print(b)

class Pilha:
    '''
    __str__ method assumes elements are not strings and can be converted to string.
    '''

    def __init__(self):
        self.lista = []

    def __iter__(self):
        for index in range(len(self.lista)-1, -1, -1):
            yield self.lista[index]

    def __len__(self):
         return len(self.lista)

    def __str__(self):
        string = []
        for element in self:
            string.append(str(element))
        return ', '.join(string)

    def push(self, multiple):
        self.lista.extend(multiple)

    def pop(self):
        if not self.lista:
            return None
        dado = self.lista[-1]
        del self.lista[-1]
        return dado

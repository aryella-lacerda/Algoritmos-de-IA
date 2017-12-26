class FilaPrioridade:
    def __init__(self, function):
        '''
        Classe genérica que recebe uma funcao f.
        f deve receber dois parametros do tipo dos elementos a serem inseridos na fila.
        f deve retornar o elemento de maior prioridade.
        '''
        self.fila = []
        self._funcaoPrioridade = function

    def __len__(self):
        return len(self.fila)

    def __iter__(self):
        for i in range(len(self)):
            yield self.fila[i]

    def __str__(self):
        string = []
        for element in self:
            string.append(str(element))
        return ', '.join(string)

    def _esquerdo(self, i):
        return 2*i + 1

    def _direito(self, i):
        return 2*i + 2

    def _pai (self, i):
        return (i-1)//2

    def _trocar(self, a, b):
        return b,a

    def _heapify (self, i):
        P = i;
        E = self._esquerdo(i);
        D = self._direito(i);

        if E < len(self) and self._funcaoPrioridade(self.fila[E], self.fila[P]): P = E
        if D < len(self) and self._funcaoPrioridade(self.fila[D], self.fila[P]): P = D

        if P != i:
            self.fila[P], self.fila[i] = self._trocar(self.fila[P], self.fila[i])
            self._heapify(P)

    def _existirPai(self, i):
        p = (i-1)/2;
        return p >= 0

    def _heapifyUp(self, i):
        while self._existirPai(i):
            self._heapify(self._pai(i));
            i = self._pai(i);

    def push(self, elements):
        '''Recebe um Elemento ou um vetor de Elementos'''
        for element in elements:
            self.fila.append(element)
            self._heapifyUp(len(self)-1)

    def pop(self):
        if not self.fila:
            return None
        toPop = self.fila[0]
        self.fila[0] = self.fila[-1]
        del self.fila[-1]   #Deletar ultimo elemento eh O(1)
        self._heapify(0)
        return toPop

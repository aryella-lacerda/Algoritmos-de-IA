# TODO: Implementar buscarVariavelNaoAtribuida()
# TODO: Implementar estadoFinal(atual)
# TODO: Implementar ordenarValoresDoDominio(var)
# TODO: Implementar atribuir(var, val, atual)
# TODO: Implementar propagar(var, val):
# TODO: Implementar removerAtribuicao(var, val, atual)
# TODO: Implementar removerPropagacao(var, val)

class Quadrado:
    def __init__(self, n = None):
        '''Recebe o n do quadrado, caso seja informado. Por segurança, n = None por padrão.'''
        self.n = n
        if self.n is None: self.dominio = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:              self.dominio = [n]

    def tamDominio(self):
        return len(self.dominio)

    def __repr__(self):
        return str(self.n)

class Sudoku:
    def __init__(self, matriz):
        '''Recebe uma matriz 9x9 do tipo inteiro para processamento.'''
        self.sudoku = self._processarMatriz(matriz)

    # A título de curiosidade, poderiamos ter feito isso:
    # return '\n'.join([' '.join([str(n) for n in lin]) for lin in self.sudoku])
    def __repr__(self):
        matrizStr = []
        for i, linha in enumerate(self.sudoku):
            linhaStr = []
            for j, quadrado in enumerate(linha):
                if j % 3 == 0 and j != 0:   linhaStr.append('|')
                if quadrado.n is not None:  linhaStr.append(str(quadrado.n))
                else:                       linhaStr.append('x')
            if i % 3 == 0 and i != 0:
                matrizStr.append('---------------------')
            matrizStr.append(' '.join(linhaStr))
        return '\n'.join(matrizStr)

    def _processarMatriz(self, matriz):
        '''Recebe uma matriz 9x9 do tipo inteiro para processamento.'''
        tabuleiroProcessado = []
        for linha in matriz:
            linhaProcessada = []
            for n in linha:
                if n != 0: elemento = Quadrado(n)
                else:      elemento = Quadrado(None)
                linhaProcessada.append(elemento)
            tabuleiroProcessado.append(linhaProcessada)
        return tabuleiroProcessado

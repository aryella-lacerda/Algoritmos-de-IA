# TODO: Implementar propagar(var, val):
# TODO: Implementar removerAtribuicao(var, val, atual)
# TODO: Implementar removerPropagacao(var, val)

from collections import namedtuple
Coordenada = namedtuple('Coordenada', 'x y')

class Quadrante:
    def __init__(self, n, linhas, colunas):
        #Os indices das 3 linhas e das 3 colunas que compõem o quadrante.
        #Para faciliar iteração pelos quadrados daquele quadrante.
        self.n = n
        self.linhas = linhas
        self.colunas = colunas

class Quadrado:
    def __init__(self, coordenada, quadrante, n = None):
        '''
        Recebe o n do quadrado, caso seja informado. Por segurança, n = None por padrão.
        Recebe uma Coordenada representado as coordenada do quadrado, e um Quadrante correspondente.
        '''
        self.n = n
        self.coordenada = coordenada
        self.quadrante = quadrante

        # Operações feitas sobre o domínio: adicionar, remover, contém/não contém
        # Dominio poderia ser representado por uma lista ou por um set.
        # Lista: append(1), remove O(n), in/not in O(n)
        # Set: add O(1), remove O(1), in/not in O(1)

        if self.n is None: self.dominio = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        else:              self.dominio = {n}

    def dominioVazio(self):
        return len(self.dominio) == 0

    def __repr__(self):
        return str(self.n)

class Sudoku:
    def __init__(self, sud):
        '''Recebe uma sud 9x9 do tipo inteiro para processamento.'''
        self._nVarNaoAtribuidas = 0;
        self._quadrantes = self._initQuadrantes()
        self.sudoku = self._processarsud(sud)

    def _initQuadrantes(self):
        quadrantes = []
        i = 0
        for linhas in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            for colunas in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                quadrantes.append( Quadrante(i, linhas, colunas) )
                i += 1
        return quadrantes

    # A título de curiosidade, poderiamos ter feito isso:
    # return '\n'.join([' '.join([str(n) for n in lin]) for lin in self.sudoku])
    # Seria mais rápido, menos legível, e sem formatação
    #O(n*m)
    def __repr__(self):
        sudStr = []
        for i, linha in enumerate(self.sudoku):
            linhaStr = []
            for j, quadrado in enumerate(linha):
                if j % 3 == 0 and j != 0:   linhaStr.append('|')
                if quadrado.n is not None:  linhaStr.append(str(quadrado))
                else:                       linhaStr.append('x')
            if i % 3 == 0 and i != 0:
                sudStr.append('---------------------')
            sudStr.append(' '.join(linhaStr))
        return '\n'.join(sudStr)

    #O(n*m)
    def _processarsud(self, sud):
        '''Recebe uma sud 9x9 do tipo inteiro para processamento.'''
        tabuleiroProcessado = []
        for i, linha in enumerate(sud):
            linhaProcessada = []
            for j, num in enumerate(linha):

                #Configurando cada Quadrado individualmente
                coord = Coordenada(i,j)
                quad = self._defQuadrante(coord)
                if num != 0:
                    elemento = Quadrado(coord, quad, num)
                else:
                    elemento = Quadrado(coord, quad, None)
                    self._nVarNaoAtribuidas += 1

                linhaProcessada.append(elemento)
            tabuleiroProcessado.append(linhaProcessada)
        return tabuleiroProcessado

    def _defQuadrante(self, coordenada):
        '''
        Recebe uma Coordenada, retorna um dos 9 Quadrantes do tabuleiro.
        '''
        x, y = coordenada
        if x >= 0 and x < 3:
            if y >= 0 and y < 3: return self._quadrantes[0]
            if y < 6: return self._quadrantes[1]
            if y < 9: return self._quadrantes[2]
        if x < 6:
            if y >= 0 and y < 3: return self._quadrantes[3]
            if y < 6: return self._quadrantes[4]
            if y < 9: return self._quadrantes[5]
        if x < 9:
            if y >= 0 and y < 3: return self._quadrantes[6]
            if y < 6: return self._quadrantes[7]
            if y < 9: return self._quadrantes[8]

    #O(n*m)
    def buscarVariavelNaoAtribuida(self):
        for linha in self.sudoku:
            for quadrado in linha:
                if quadrado.n is None:
                    return quadrado
        return None

    #O(1)
    def estadoFinal(self):
        return self._nVarNaoAtribuidas == 0

    def ordenarValoresDoDominio(self, var):
        '''
        Recebe uma variável do tipo Quadrado.
        Retorna uma lista com seu domínio, ordenado.
        '''
        #Uma heuristica é escolher o valor que causa menos restrições nas demais variáveis. Inicialmente sem ordenação, porque isso parece complicado de implementar.
        #LCV - Least Constraining Value
        return var.dominio

    def atribuir(self, var, val):
        var.n = val
        self._nVarNaoAtribuidas -= 1

    def dominioContem(self, quadrado, val):
        return quadrado.n is None and val in quadrado.dominio

    def propagar(self, var, val):
        # Readability
        x, y = var.coordenada
        sud = self.sudoku
        q = var.quadrante

        #Procurar val no dominio das variáveis não atribuídas daquela linha e remover
        linha = [quad for quad in sud[x] if dominioContem(quad, val)]
        for quadrado in linha:
            quadrado.dominio.remove(val)
            if quadrado.dominioVazio():
                return False

        #Procurar val no dominio das variáveis não atribuídas daquela coluna e remover
        coluna = [sud[i][y] for i in range(9) if dominioContem(sud[i][y], val)]
        for quadrado in coluna:
            quadrado.dominio.remove(val)
            if quadrado.dominioVazio():
                return False

        #Procurar val no dominio das variáveis não atribuídas daquele quadrante e remover
        quadrante = [sud[i][j] for i in q.linhas for j in q.colunas if dominioContem(sud[i][j], val)]
        for quadrado in quadrante:
            quadrado.dominio.remove(val)
            if quadrado.dominioVazio():
                return False

        return True

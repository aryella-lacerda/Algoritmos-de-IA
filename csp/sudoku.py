from collections import namedtuple
from pilha import Pilha
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
        self.retirado = Pilha()

        # Operações feitas sobre o domínio: adicionar, remover, contém/não contém
        # Dominio poderia ser representado por uma lista ou por um set.
        # Lista: append(1), remove O(n), in/not in O(n)
        # Set: add O(1), remove O(1), in/not in O(1)

        if self.n is None: self.dominio = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        else:              self.dominio = {n}

    def dominioVazio(self):
        return len(self.dominio) == 0

    def dominioUnico(self):
        return len(self.dominio) == 1

    def __repr__(self):
        if self.n is None:
            return f"x - {self.dominio}"
        return f"{self.n} - {self.dominio}"

class Sudoku:
    def __init__(self, sud):
        '''Recebe uma sud 9x9 do tipo inteiro para processamento.'''
        self._nVarNaoAtribuidas = 0;
        self._iniciais = []
        self._quadrantes = self._initQuadrantes()
        self.sudoku = self._processarMatriz(sud)

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
                if j % 3 == 0 and j != 0:
                    linhaStr.append('|')
                linhaStr.append(str(quadrado))
            if i % 3 == 0 and i != 0:
                sudStr.append('---------------------')
            sudStr.append(' '.join(linhaStr))
        return '\n'.join(sudStr)

    #O(n*m)
    def _processarMatriz(self, sud):
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
                    self._iniciais.append(elemento)
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
        #No caso de propagação e atribuição automática de valores, o último valor restante no domínio é retirado para ser atribuido, e então deve ser reinserido no dominio.
        if val in var.dominio:
            var.dominio.remove(val)
        else:
            var.dominio.add(val)


    def removerAtribuicao(self, var):
        var.n = None
        self._nVarNaoAtribuidas += 1

    def aplicarPropagacaoInicial(self):
        for quadrado in self._iniciais:
            self.propagar(quadrado, quadrado.n)

    def _dominioContem(self, quadrado, val):
        return quadrado.n is None and val in quadrado.dominio

    def _retiradoContem(self, quadrado, val):
        return quadrado.retirado.top == val

    def _removerValorDoDominio(self, lista, val):
        '''
        Recebe uma lista contendo os Quadrados cujos dominios serão alerados.
        Se restar somente um valor no domínio de alguma variável,
        Retorna True somente se alguma variável ficar com domínio vazio.
        Caso contrário, retorna None.
        '''
        for quadrado in lista:
            quadrado.dominio.remove(val)
            quadrado.retirado.push(val)
            if quadrado.dominioVazio():
                return True
            # Se restar somente um val no domínio
            if quadrado.dominioUnico():
                self.atribuir(quadrado, quadrado.dominio.pop())

    def _reinserirValorNoDominio(self, lista, val):
        '''
        Recebe uma lista cujos quadrados cujo topo da pilha de retirados é o val.
        Retira o topo da pilha, e reinsire-o no dominio.
        '''
        for quadrado in lista:
            quadrado.retirado.pop()
            quadrado.dominio.add(val)

    def propagar(self, var, val):
        '''
        Recebe um Quadrado (var) e um dígito (val).
        Se a propagação concluir sem erro, retorna True.
        Se a propagação gerar uma variável com domínio vazio, retorna False.
        '''

        # Readability
        x, y = var.coordenada
        sud = self.sudoku
        q = var.quadrante

        # Procurar val no dominio das variáveis não atribuídas daquela linha/coluna/quadrante e separar essas variáveis
        # Retorna false se alguma variável ficar com dominio vazio.
        linha = [quad for quad in sud[x] if self._dominioContem(quad, val)]
        if self._removerValorDoDominio(linha, val):
            return False

        coluna = [sud[i][y] for i in range(9) if self._dominioContem(sud[i][y], val)]
        if self._removerValorDoDominio(coluna, val):
            return False

        quadrante = [sud[i][j] for i in q.linhas
                               for j in q.colunas
                               if self._dominioContem(sud[i][j], val)]
        if self._removerValorDoDominio(quadrante, val):
            return False

        return True

    def removerPropagacao(self, var, val):
        '''
        Recebe um Quadrado (var) e um dígito (val).
        '''
        #Readability
        x, y = var.coordenada
        sud = self.sudoku
        q = var.quadrante

        #Separar, em cada caso (linha/coluna/quadrante), os quadrados na qual o val for retirado mais recentemente.
        linha = [quad for quad in sud[x] if self._retiradoContem(quad, val)]
        self._reinserirValorNoDominio(linha, val)

        coluna = [sud[i][y] for i in range(9) if self._retiradoContem(sud[i][y], val)]
        self._reinserirValorNoDominio(coluna, val)

        quadrante = [sud[i][j] for i in q.linhas
                               for j in q.colunas
                               if self._retiradoContem(sud[i][j], val)]
        self._reinserirValorNoDominio(quadrante, val)

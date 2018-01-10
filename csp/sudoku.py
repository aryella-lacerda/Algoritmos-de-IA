from collections import namedtuple
from pilha import Pilha
from fila import Fila
from random import randint, choice
from math import inf
from itertools import chain

class Quadrante:
    '''Existe para faciliar a iteração pelos vars daquela coluna.'''

    def __init__(self, linhas, colunas):
        '''Recebe duas listas contendo os indices das 3 linhas e das 3 colunas que compõem o quadrante.'''
        self.linhas = linhas
        self.colunas = colunas

class Quadrado:
    def __init__(self, coordenada, quadrante, n = None):
        '''Recebe uma coordenada e um Quadrante correspondente. Se o valor n inicial não for informado, o padrão é None.'''
        self.n = n
        self.coordenada = coordenada
        self.quadrante = quadrante
        self.retirados = Pilha()
        self.conflitos = 0

        # Operações feitas sobre o domínio: adicionar, remover, contém/não contém
        # Dominio poderia ser representado por uma lista ou por um set.
        # Lista: append(1), remove O(n), in/not in O(n)
        # Set: add O(1), remove O(1), in/not in O(1)

        if self.n is None: self.dominio = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        else:              self.dominio = {n}

    def dominioVazio(self):
        return len(self.dominio) == 0

    def __repr__(self):
        if self.n is None:
            return f"[x -> {self.conflitos}]"
        return f"[{self.n} -> {self.conflitos}]"

class Estado:
    def __init__(self, var):
        '''Recebe um Quadrado.'''
        self.var = var
        self.afetadosPelaPropagacao = []

    def __repr__(self):
        return f"{self.var} - Propagados: {self.afetadosPelaPropagacao}"

class Sudoku:

    def __init__(self, sud):
        '''Recebe uma sud 9x9 do tipo inteiro para processamento.'''
        self._countNaoAtribuidas = 0
        self._countConflitos = 0
        self._iniciais = set()
        self._quadrantes = self._initQuadrantes()
        self._estadoAtual = None
        self._propagacaoInicial = True
        self.sudoku = self._processarMatriz(sud)

    #O(1)
    def _initQuadrantes(self):
        quadrantes = []
        for linhas in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            for colunas in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                quadrantes.append( Quadrante(linhas, colunas) )
        return quadrantes

    #O(n*m)
    def __repr__(self):
        sudStr = []
        for i, linha in enumerate(self.sudoku):
            linhaStr = []
            for j, var in enumerate(linha):
                if j % 3 == 0 and j != 0:
                    linhaStr.append('|')
                linhaStr.append(str(var))
            if i % 3 == 0 and i != 0:
                sudStr.append('---------------------')
            sudStr.append(' '.join(linhaStr))
        return '\n'.join(sudStr)

    #O(n*m)
    def _processarMatriz(self, sud):
        '''Recebe uma matriz 9x9 do tipo inteiro para processamento.'''

        tabuleiroProcessado = []
        for i, linha in enumerate(sud):
            linhaProcessada = []
            for j, num in enumerate(linha):

                #Configurando cada Quadrado individualmente
                coor = (i,j)
                quad = self._defQuadrante(coor)
                if num != 0:
                    elemento = Quadrado(coor, quad, num)
                    self._iniciais.add(elemento)
                else:
                    elemento = Quadrado(coor, quad, None)
                    self._countNaoAtribuidas += 1

                linhaProcessada.append(elemento)
            tabuleiroProcessado.append(linhaProcessada)
        return tabuleiroProcessado

    def _defQuadrante(self, coordenada):
        '''Recebe uma coordenada, retorna um dos 9 Quadrantes do tabuleiro.'''
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


#-----------------------------------------------

# HIDDEN SINGLE
#-----------------------------------------------

    #0(1)
    def _verificarSingularidade(self, conjunto, n):
        '''Recebe um iterável e um dígito.'''
        conjunto = (var for var in conjunto if (n in var.dominio and var.n is None))
        singularidade = None
        for i, element in enumerate(conjunto):
            if i == 0:
                singularidade = element
            else:
                singularidade = None
                break
        return singularidade

    def atribuirSingularidade(self, var, val):
        self.atribuir(var, val)
        self.propagar(var, val)

    def _aplicar(self, conjunto):
        for num in range(1,10):
            singular = self._verificarSingularidade(conjunto, num)
            if singular:
                self.atribuirSingularidade(singular, num)

    #O(m*n) - passa 3 vezes pelo tabuleiro
    def _hiddenSingleInicial(self):

        for i in range(9):

            q = self._quadrantes[i]
            lin = [self.sudoku[i][j] for j in range(9)] #Linha i
            col = [self.sudoku[j][i] for j in range(9)] #Coluna i
            qua = [self.sudoku[a][b] for a in q.linhas  #Quadrante i
                                     for b in q.colunas]

            self._aplicar(lin)
            self._aplicar(col)
            self._aplicar(qua)

    def printThis(self, lista):
        for x in lista:
            print(x)

#-----------------------------------------------
# FUNÇÕES MÍNIMOS CONFLITOS
#-----------------------------------------------

# FUNÇÕES MÍNIMOS CONFLITOS
#-----------------------------------------------

    def _getConjunto(self, var, filtrar):
        ''' Recebe um Quadrado e uma função de filtro.'''

        x, y = var.coordenada

        lin = (self.sudoku[x][i] for i in range(9) if filtrar(self.sudoku[x][i]))
        col = (self.sudoku[i][y] for i in range(9) if filtrar(self.sudoku[i][y]))
        qua = (self.sudoku[i][j] for i in var.quadrante.linhas \
                                 for j in var.quadrante.colunas \
                                 if filtrar(self.sudoku[i][j]))

        return chain(lin, col, qua)

    def _getConjunto(self, var, filtrar):
        ''' Recebe um Quadrado e uma função de filtro.'''

        x, y = var.coordenada

        lin = (self.sudoku[x][i] for i in range(9) if filtrar(self.sudoku[x][i]))
        col = (self.sudoku[i][y] for i in range(9) if filtrar(self.sudoku[i][y]))
        qua = (self.sudoku[i][j] for i in var.quadrante.linhas \
                                 for j in var.quadrante.colunas \
                                 if filtrar(self.sudoku[i][j]))

        return chain(lin, col, qua)

    def _definirConflitos(self):
        for linha in self.sudoku:
            for var in linha:
                if var not in self._iniciais:
                    var.conflitos = self._getConflitos(var)
                    self._countConflitos += var.conflitos

    def _definirValores(self):
        for linha in self.sudoku:
            for var in linha:
                if var not in self._iniciais:
                    var.n = choice(tuple(var.dominio))
                    self._countNaoAtribuidas -= 1

    def atribuirEstadoAleatorio(self):
        self._definirValores()
        self._definirConflitos()

    def atribuirMC(self, var, novo, conf):
        antigo = var.n
        self._countConflitos -= var.conflitos
        var.n = novo
        var.conflitos = conf
        self._countConflitos += var.conflitos
        self._updateConflitos(var, novo, antigo)

    def _updateConflitos(self, var, valNovo, valAntigo):

        #Definir filtro dependendo dos valores novo e antigo da variável atual
        def _filtrar(elemento):
            ''' Recebe dois inteiros. '''
            return ((elemento.n == valNovo or elemento.n == valAntigo) and elemento != var)

        #Receber conjunto filtrado
        conjunto = self._getConjunto(var, _filtrar)

        #Recalcular conflitos somente para os elementos relevantes.
        for elem in conjunto:
            nAntigo = elem.conflitos
            nNovo = self._getConflitos(elem)
            elem.conflitos = nNovo
            self._countConflitos -= nAntigo
            self._countConflitos += nNovo

    def varEmConflito(self):
        while True:
            var = self.sudoku[randint(0,8)][randint(0,8)]
            if var.conflitos > 0:
                return var

    def valQueMinizaConflito(self, var):
        minVal = None
        minConf = inf
        for val in var.dominio:
            conf = self._getConflitos(var, val)
            if conf < minConf:
                minConf = conf
                minVal = val

        if minVal == var.n:
            minVal = choice(tuple(var.dominio))
            minConf = self._getConflitos(var, minVal)

        return (minVal, minConf)

    def _getConflitos(self, var, n = None):

        if n:
            def _filtrar(elem):
                return (elem.n and n == elem.n and var != elem)
        else:
            def _filtrar(elem):
                return (var.n and elem.n and var.n == elem.n and var != elem)

        conflitos = 0
        for elem in self._getConjunto(var, _filtrar):
            conflitos += 1

        return conflitos

#-----------------------------------------------
# FUNÇÕES BACKTRACKING
#-----------------------------------------------

    def aplicarPropagacaoInicial(self):
        for var in self._iniciais:
            self.propagar(var, var.n)

        self._hiddenSingleInicial()
        self._propagacaoInicial = False

    #O(n*m)
    def buscarVariavelNaoAtribuida(self):
        for linha in self.sudoku:
            for var in linha:
                if var.n is None:
                    return var
        return None

    #O(1)
    def estadoFinal(self):
        return not self._countNaoAtribuidas and not self._countConflitos

    def ordenarValoresDoDominio(self, var):
        '''
        Recebe uma variável do tipo Quadrado.
        Retorna uma lista com seu domínio, ordenado.
        '''
        #Uma heuristica é escolher o valor que causa menos restrições nas demais variáveis. Inicialmente sem ordenação, porque isso parece complicado de implementar.
        #LCV - Least Constraining Value
        return var.dominio.copy()

#-----------------------------------------------
# SEQUÊNCIA DE PASSOS PARA ATRIBUIR E PROPAGAR
#-----------------------------------------------

    def atribuir(self, var, val, estado = None):
        ''' Recebe um Quadrado, um dígito, e um Estado.'''

        #Setar o estado
        self._estadoAtual = estado
        self._countNaoAtribuidas -= 1
        if not self._propagacaoInicial:
            self._estadoAtual.afetadosPelaPropagacao = []
        else:
            self._iniciais.add(var)

        #Setar os valores retirados do domínio pela atribuição
        var.dominio.remove(val)
        var.retirados.push(var.dominio)

        #Setar domínio de atribuição (o próprio val)
        var.dominio = {val}
        var.n = val

    def propagar(self, var, val):
        '''Recebe um Quadrado e um dígito.'''

        def _filtrar(elemento):
            return (elemento.n is None and val in elemento.dominio)


        def _filtrar(elemento):
            return (elemento.n is None and val in elemento.dominio)

        conjunto = self._getConjunto(var, _filtrar)

        # Retorna True (Falha!) se alguma variável ficar com dominio vazio.
        if self._removerValorDoDominio(conjunto, val):
            return False

        return True

    def _removerValorDoDominio(self, conjunto, val):
        '''
        Recebe um iterável.
        Retorna True somente se alguma variável ficar com domínio vazio.
        Caso contrário, retorna None.
        '''
        for var in conjunto:
            var.dominio.remove(val)

            # Ou seja, se essa for uma propagação diferente da inicial
            if self._estadoAtual is not None:
                self._estadoAtual.afetadosPelaPropagacao.append(var)

            # Se restão nenhum valor no domínio, gerar erro.
            if var.dominioVazio():
                return True

#------------------------------------------------------------------------------
# SEQUÊNCIA DE PASSOS PARA DESFAZER ATRIBUIÇÃO E PROPAGAÇÃO
#------------------------------------------------------------------------------

    def restaurar(self, estado):
        self._estadoAtual = estado
        self._removerPropagacao(estado.afetadosPelaPropagacao, estado.var.n)
        self._removerAtribuicao(estado.var)

    def _removerPropagacao(self, afetados, val):
        for var in afetados:
            var.dominio.add(val)
        afetados = []

    def _removerAtribuicao(self, var):
        var.n = None
        reinserir = var.retirados.pop()
        # Se houver o que reinserir...
        if reinserir:
            var.dominio.update(reinserir)
        self._countNaoAtribuidas += 1

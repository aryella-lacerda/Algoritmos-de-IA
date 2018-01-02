from collections import namedtuple
from pilha import Pilha
from fila import Fila
Coordenada = namedtuple('Coordenada', 'x y')

class Quadrante:
    '''
    Existe para faciliar a iteração pelos vars daquela coluna.
    '''
    def __init__(self, linhas, colunas):
        #Os indices das 3 linhas e das 3 colunas que compõem o quadrante.
        #Para faciliar iteração pelos vars daquele quadrante.
        self.linhas = linhas
        self.colunas = colunas

class Quadrado:
    def __init__(self, coordenada, quadrante, n = None):
        '''
        Recebe o n do var, caso seja informado. Por segurança, n = None por padrão.
        Recebe uma Coordenada representado as coordenada do var, e um Quadrante correspondente.
        '''
        self.n = n
        self.coordenada = coordenada
        self.quadrante = quadrante
        self.retirados = Pilha()

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
            return f"x - {self.dominio}"
        return f"{self.n}"

class Estado:
    def __init__(self, var):
        '''
        Recebe um Quadrado.
        '''
        self.var = var
        self.afetadosPelaPropagacao = []

    def __repr__(self):
        return f"{self.var} - Propagados: {self.afetadosPelaPropagacao}"

class Sudoku:

    def __init__(self, sud):
        '''Recebe uma sud 9x9 do tipo inteiro para processamento.'''
        self._countNaoAtribuidas = 0;
        self._iniciais = []
        self._quadrantes = self._initQuadrantes()
        self._estadoAtual = None
        self.sudoku = self._processarMatriz(sud)

    def _initQuadrantes(self):
        quadrantes = []
        for linhas in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            for colunas in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                quadrantes.append( Quadrante(linhas, colunas) )
        return quadrantes

    # A título de curiosidade, poderiamos ter feito isso:
    # return '\n'.join([' '.join([str(n) for n in lin]) for lin in self.sudoku])
    # Seria mais rápido, menos legível, e sem formatação
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
                    self._countNaoAtribuidas += 1

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

#-----------------------------------------------
# TÉCNICAS DE PROPAGAÇÃO
#-----------------------------------------------

    def existirSingularidade(self, lista, num):
        '''
        Recebe uma lista de Quadrados e um dígito.
        '''
        vars = [var for var in lista if num in var.dominio]
        if len(vars) == 1:
            return vars[0] #True

    def atribuirSingularidade(self, var, val):
        self.atribuir(var, val)
        self.propagar(var, val)

    def applicarLinColQuad(self, linha, coluna, quadrante):
        for num in range(1,10):
            singular = self.existirSingularidade(linha, num)
            if singular:
                self.atribuirSingularidade(singular, num)

            singular = self.existirSingularidade(coluna, num)
            if singular:
                self.atribuirSingularidade(singular, num)

            singular = self.existirSingularidade(quadrante, num)
            if singular:
                self.atribuirSingularidade(singular, num)

    # def hiddenSingle(self, var):
    #     x, y = var.coordenada
    #     sud = self.sudoku
    #     q = var.quadrante
    #
    #     linha = [var for var in sud[x]]
    #     coluna = [sud[i][y] for i in range(9)]
    #     quadrante = [sud[i][j] for i in q.linhas for j in q.colunas]
    #
    #     self.applicarLinColQuad(linha, coluna, quadrante)

    def hiddenSingleInicial(self):
        sud = self.sudoku
        for i in range(9):

            q = self._quadrantes[i]
            linha = [var for var in sud[i]] #Linha i
            coluna = [sud[i][j] for j in range(9)]  #Coluna i
            quadrante = [sud[a][b] for a in q.linhas for b in q.colunas] #Quadrante i

            self.applicarLinColQuad(linha, coluna, quadrante)

#-----------------------------------------------
# FUNÇÕES BACKTRACKING
#-----------------------------------------------

    def aplicarPropagacaoInicial(self):
        for var in self._iniciais:
            self.propagar(var, var.n)
        self.hiddenSingleInicial()

    #O(n*m)
    def buscarVariavelNaoAtribuida(self):
        for linha in self.sudoku:
            for var in linha:
                if var.n is None:
                    return var
        return None

    #O(1)
    def estadoFinal(self):
        return self._countNaoAtribuidas == 0

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
        '''
        Recebe um objeto Quadrado, um dígito, e um objeto Estado.
        '''
        #Setar o estado
        self._estadoAtual = estado
        if estado is not None:
            self._estadoAtual.afetadosPelaPropagacao = []
        self._countNaoAtribuidas -= 1

        #Setar os valores retirados do domínio pela atribuição
        var.dominio.remove(val)
        var.retirados.push(var.dominio)

        #Setar domínio de atribuição (o próprio val)
        var.dominio = {val}
        var.n = val

    def foundError(self, var):
        x, y = var.coordenada

        # Separar linha/coluna/quadrante referentes àquela variável
        linha = [quad for quad in self.sudoku[x]]
        coluna = [self.sudoku[i][y] for i in range(9)]
        quadrante = [self.sudoku[i][j] for i in var.quadrante.linhas for j in var.quadrante.colunas]

        if self.error(linha): return True
        if self.error(coluna): return True
        if self.error(quadrante): return True

    def error(self, lista):
        for i in range(1,10):
            rep = 0
            for quad in lista:
                if quad.n == i:
                    rep += 1
            if rep > 1:
                return True
        return False

    def propagar(self, var, val):
        '''
        Recebe um Quadrado (var) e um dígito (val).
        '''
        x, y = var.coordenada

        # Separar linha/coluna/quadrante referentes àquela variável
        linha = [quad for quad in self.sudoku[x]]
        coluna = [self.sudoku[i][y] for i in range(9)]
        quadrante = [self.sudoku[i][j] for i in var.quadrante.linhas for j in var.quadrante.colunas]

        # Retorna True (Falha!) se alguma variável ficar com dominio vazio.
        if self._removerValorDoDominio(linha, val):
            return False
        if self._removerValorDoDominio(coluna, val):
            return False
        if self._removerValorDoDominio(quadrante, val):
            return False

        return True

    def _dominioContem(self, var, val):
        return var.n is None and val in var.dominio

    def _removerValorDoDominio(self, lista, val):
        '''
        Recebe uma lista de Quadrados.
        Retorna True somente se alguma variável ficar com domínio vazio.
        Caso contrário, retorna None.
        '''
        for var in lista:

            #Retirar val somente dos vars em que val esteja no dominio.
            if self._dominioContem(var, val):
                var.dominio.remove(val)

                # Ou seja, se essa for uma propagação diferente da inicial
                if self._estadoAtual is not None:
                    self._estadoAtual.afetadosPelaPropagacao.append(var)
                    #var.retirados.push({val})

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

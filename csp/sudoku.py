from collections import namedtuple
from pilha import Pilha
from fila import Fila
Coordenada = namedtuple('Coordenada', 'x y')
Propagacao = namedtuple('Propagacao', 'atribuidosAutomaicamente falha')

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
        self.retirados = Pilha()

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
        return f"{self.n}"

class Sudoku:

    def __init__(self, sud):
        '''Recebe uma sud 9x9 do tipo inteiro para processamento.'''
        self._nVarNaoAtribuidas = 0;
        self._iniciais = []
        self._quadrantes = self._initQuadrantes()
        self._espera = Fila()
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

#-----------------------------------------------
# TÉCNICAS DE PROPAGAÇÃO
#-----------------------------------------------

    def existirSingularidade(self, lista, num):
        '''
        Recebe uma lista de Quadrados e um dígito.
        '''
        quadrados = [quadrado for quadrado in lista if num in quadrado.dominio]
        if len(quadrados) == 1:
            return quadrados[0] #True

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

    def hiddenSingle(self, var):
        x, y = var.coordenada
        sud = self.sudoku
        q = var.quadrante

        linha = [quadrado for quadrado in sud[x]]
        coluna = [sud[i][y] for i in range(9)]
        quadrante = [sud[i][j] for i in q.linhas for j in q.colunas]

        self.applicarLinColQuad(linha, coluna, quadrante)

    def hiddenSingleInicial(self):
        sud = self.sudoku
        for i in range(9):

            q = self._quadrantes[i]
            linha = [quadrado for quadrado in sud[i]] #Linha i
            coluna = [sud[i][j] for j in range(9)]  #Coluna i
            quadrante = [sud[a][b] for a in q.linhas for b in q.colunas] #Quadrante i

            self.applicarLinColQuad(linha, coluna, quadrante)

#-----------------------------------------------
# ALGORITMOS BACKTRACKING
#-----------------------------------------------

    def aplicarPropagacaoInicial(self):
        for quadrado in self._iniciais:
            self.propagar(quadrado, quadrado.n)
        self.hiddenSingleInicial()

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

#-----------------------------------------------
# SEQUÊNCIA DE PASSOS PARA ATRIBUIR E PROPAGAR
#-----------------------------------------------

    def atribuir(self, var, val):
        '''
        Recebe um objeto Quadrado e um dígito.
        '''
        var.dominio.remove(val)
        var.retirados.push(var.dominio)
        var.n = val
        self._nVarNaoAtribuidas -= 1

    def _atribuirAutomatico(self, var, val):
        #No caso de propagação e atribuição automática de valores, o último valor restante no domínio é retirados para ser atribuido, e então deve ser reinserido no dominio. Única dificuldade da estrutura 'set'.
        var.n = val
        self._nVarNaoAtribuidas -= 1
        var.dominio.add(val)

    def propagar(self, var, val):
        '''
        Recebe um Quadrado (var) e um dígito (val).
        Se a propagação concluir sem erro, retorna Propagacao(atribuicoesAutomaticas, true).
        Se a propagação gerar uma variável com domínio vazio, retorna Propagacao(atribuicoesAutomaticas, false).
        '''

        # Readability
        x, y = var.coordenada
        sud = self.sudoku
        q = var.quadrante

        atribuicoesAutomaticas = []

        # Procurar val no dominio das variáveis não atribuídas daquela linha/coluna/quadrante e separar essas variáveis.
        linha = [quad for quad in sud[x]]
        coluna = [sud[i][y] for i in range(9)]
        quadrante = [sud[i][j] for i in q.linhas for j in q.colunas]

        # Retorna True(Falha!) se alguma variável ficar com dominio vazio.
        # Se encontrar algum domínio único, inclui na lista de espera.
        # Ou seja, nesse momento, nenhuma atribuição automática foi feita ainda.
        if self._removerValorDoDominio(linha, val):
            return Propagacao([], True)

        if self._removerValorDoDominio(coluna, val):
            return Propagacao([], True)

        if self._removerValorDoDominio(quadrante, val):
            return Propagacao([], True)

        #CASO: atribuições automáticas de variáveis com domínio únicos.
        if len(self._espera) != 0:

            prox = self._espera.pop()
            atribuicoesAutomaticas.append(prox)

            self._atribuirAutomatico(prox, prox.dominio.pop())
            resultado = self.propagar(prox, prox.n):

            if resultado.falha:
                atribuicoesAutomaticas.extend(resultado.atribuicoesAutomaticas)
                return Propagacao(atribuicoesAutomaticas, True)

        print(self)
        return Propagacao(atribuicoesAutomaticas, False)

    def _dominioContem(self, var, val):
        return var.n is None and val in var.dominio

    def _removerValorDoDominio(self, lista, val):
        '''
        Recebe uma lista de Quadrados.
        Se restar somente um valor no domínio de alguma variável, coloca na lista de espera p/ atribuir automaticamente.
        Retorna True somente se alguma variável ficar com domínio vazio.
        Caso contrário, retorna None.
        '''
        for quadrado in lista:

            #Retirar val somente dos quadrados em que val esteja no dominio.
            if self._dominioContem(quadrado, val):
                quadrado.dominio.remove(val)
                quadrado.retirados.push([val])

                # Se restão nenhum valor no domínio, gerar erro.
                if quadrado.dominioVazio():
                    return True

                # Se restar somente um val no domínio, atribuir automaticamente
                if quadrado.dominioUnico():
                    self._espera.push(quadrado)

#------------------------------------------------------------------------------
# SEQUÊNCIA DE PASSOS PARA DESFAZER ATRIBUIÇÃO E PROPAGAÇÃO
#------------------------------------------------------------------------------

    def removerAtribuicao(self, var):
        #Se a atribuição precisou ser retirada, não há porque devolvê-la para o dominio.
        var.dominio.update(var.retirados.pop())
        var.n = None
        self._nVarNaoAtribuidas += 1

    def _removerAtribuicaoAutomatica(self, var):
        var.n = None
        self._nVarNaoAtribuidas += 1

    def removerPropagacao(self, var, val):
        '''
        Recebe um Quadrado (var) e um dígito (val).
        '''
        #Readability
        x, y = var.coordenada
        sud = self.sudoku
        q = var.quadrante

        #Separar linha/coluna/quadrante.
        linha = [quad for quad in sud[x]]
        coluna = [sud[i][y] for i in range(9)]
        quadrante = [sud[i][j] for i in q.linhas for j in q.colunas]

        self._reinserirValorNoDominio(linha, val)
        self._reinserirValorNoDominio(coluna, val)
        self._reinserirValorNoDominio(quadrante, val)

    def _retiradosContem(self, quadrado, val):
        return val in quadrado.retirados.top

    def _reinserirValorNoDominio(self, lista, val):
        '''
        Recebe uma lista cujos quadrados cujo topo da pilha de retirados é o val.
        Retira o topo da pilha, e reinsire-o no dominio.
        '''
        for quadrado in lista:

            # Se val for o último valor retirados do domínio desse quadrado
            if self._retiradosContem(quadrado, val):
                reinserir = quadrado.retirados.pop()
                quadrado.dominio.add(reinserir)

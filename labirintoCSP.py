from collections import namedtuple
from pilha import Pilha
Tupla = namedtuple('Tupla', 'n m')

class Elemento:
    def __init__(self, elemento, indice):
        self.atribuicao = None
        self._indice = indice
        self._elemento = elemento
        self._dominio = [True, False]
        self._removidos = Pilha()

class LabirintoCSP:
    def __init__(self, nLinhas, nColunas, labirinto):
        self._dimensoes = Tupla(nLinhas, nColunas)
        self._nVariaveis = nLinhas * nColunas
        self._labirinto = labirinto
        self.inicio = None
        self.fim = None
        self._processarLabirinto()

    def _processarLabirinto(self):
        labirintoProcessado = []
        for n, linha in enumerate(self._labirinto):
            linhaProcessada = []
            for m, elemento in enumerate(linha):
                atual = Elemento(elemento, Tupla(n,m))
                if elemento == '@': self.inicio = atual
                if elemento == '$': self.fim = atual
                linhaProcessada.append(atual)
            labirintoProcessado.append(linhaProcessada)

    def _naoUltrapassaBordas(self, n, m):
        return n > -1 and n < self._dimensoes.n and m > -1 and m < self._dimensoes.m

    def _naoPossuiAtribuicao(self, n, m):
        return self._labirinto[n][m].atribuicao == None

    def buscarVariavelNaoAtribuida(self, atual):
        if atual is None:
            return self.inicio
        if self._naoUltrapassaBordas(n-1, m) and self._naoPossuiAtribuicao(n-1, m):
            return self._labirinto[n-1][m]
        if self._naoUltrapassaBordas(n, m+1) and self._naoPossuiAtribuicao(n, m+1):
            return self._labirinto[n][m+1]
        if self._naoUltrapassaBordas(n+1, m) and self._naoPossuiAtribuicao(n+1, m):
            return self._labirinto[n+1][m]
        if self._naoUltrapassaBordas(n, m-1) and self._naoPossuiAtribuicao(n, m+1):
            return self._labirinto[n][m-1]

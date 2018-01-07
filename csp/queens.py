from collections import namedtuple
Index = namedtuple('Index','n m')

class Element:
    def __init__(self, element, index):
        self.element = element
        self.index = index
        self.conflicts = 0

    def __str__(self):
        return f'{self.element}'

    def __iter__(self):
        for i in range(1):
            yield self

    __repr__ = __str__


class Queens:

    def __init__(self, lines, columns, gameBoard):
        #Private
        self._dimensions = Index(lines,columns)
        self._gameBoard = gameBoard

        #Public
        self.conflictsLine = None
        self.conflictsColumns = None

        #Procedures
        self._processGameBoard()

    def __str__(self):
        totalLines = []
        for line in self._gameBoard:
            currentLine = []
            for element in line:
                currentLine.append(str(element.element))
            totalLines.append(' '.join(currentLine))
        return '\n'.join(totalLines)

    def _processGameBoard(self):
        processedGame = []
        for n, line in enumerate(self._gameBoard):
            currentLine = []
            for m, element in enumerate(line):
                currentElement = Element(element,Index(n,m))
                currentLine.append(currentElement)
                #if element == '1': self.queen = currentElement #encontrar uma rainha

                #talvez precise colocar uma funcao pra saber os conflitos aqui
            processedGame.append(currentLine)
            self._gameBoard = processedGame

    '''
        talvez facilite tratar colunas como linha e linhas como coluna
        como em python se faz lista de Lista e.g
        [[....],[....],[....],[....]]
        deixando mais visual
        [
            [....],
            [....],
            [....],
            [....]
        ]
        cada lista dentro da lista seria uma coluna, pois nesse problema
        nao pode por duas rainhas na mesma linhas
        dai ja limita muito o espaço de busca
    '''
    def horizontalCheck(self, line): #line é uma lista
        return sum(line) #se for  > 1 tem alguma rainha na horizontal

    '''talvez essa parte aqui nem precise
    def verticalCheck(self,column): #line é uma lista
        return sum(column) # se for > 1 tem alguma rainha na vertica
    '''
    def attacks(column, i ,j):
        #quando coloca uma rainha rainha em uma linha ela passa a ser ignorada
        #por isso verificar coluna
        if column[i] == column[j]: return True
        if abs(i-j) == abs(column[i] - column[j]): return True
        return False

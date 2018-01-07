from collections import namedtuple
Index = namedtuple('Index','n m')

class Element:
    def __init__(self, element, index):
        self.element = element
        self.index = index
        self.conflicts = 0

class Queens:

    def __init__(self, lines, columns, gameBoard):
        #Private
        self._dimensions = Index(lines,columns)
        self._gameBoard = gameBoard

        #Public
        self.queen = None


    def _processGameBoard(self):
        processedGame = []
        for n, line in enumerate(self._gameBoard):
            currentLine = []
            for m, element in enumerate(line):
                currentElement = Element(element,Index(n,m))
                currentLine.append(currentElement)
                if elemen == '1': self.queen = currentElement #encontrar uma rainha

                #talvez precise colocar uma funcao pra saber os conflitos aqui

            processedGame.append(currentLine)

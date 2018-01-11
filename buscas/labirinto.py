from collections import namedtuple
from math import sqrt, fabs, inf
from random import randint
Index = namedtuple('Index', 'n m')

class Element:
    def __init__(self, element, index, weight):
        ''' Recieves an element (string), a named 2-tuple (n=int, m=int) index, and a weight value, in that order. '''
        self.element = element
        self.index = index
        self.moves = []
        self.visited = False

        #Custo uniforme
        self.weight = weight #Custo de chegar ate ele
        self.weightOfLeastCostlyPath = inf

        #Heuristica gulosa
        self.distMan = 0
        self.distEuc = 0

    def __str__(self):
        return f"{self.element}"

    def __iter__(self):
        for i in range(1):
            yield self

    __repr__ = __str__

class Labirinto:
    def __init__(self, lines, columns, _labrinth):
        '''
        Receives the _labrinth's number of lines and columns, both of type int.
        Receives the _labrinth in the form of a bidimensional list of single-char strings.
        '''

        #Private
        self._dimensions = Index(lines, columns)
        self._labrinth = _labrinth
        self._finalState = None
        self._costOfReachingLastExploredElement = 0
        self._totalExpansions = 0
        self._totalCostOfSolution = 0
        self._nOfStepsInSolution = 0

        #Public
        self.estadoInicial = None
        self.solution = None

        #Procedures
        self._processLabrinth()

    def __str__(self):
        totalLines = []
        for line in self._labrinth:
            currentLine = []
            for element in line:
                currentLine.append(str(element))
            totalLines.append(' '.join(currentLine))
        return '\n'.join(totalLines)

    def _permittedSpace(self, candidate):
        return ((not candidate.element == '#') and candidate.visited == False)

    def _implementSolution(self):
        current = self.estadoInicial
        for move in self.solution:
            n, m = current.index
            if move == '^': n -= 1
            if move == '>': m += 1
            if move == 'v': n += 1
            if move == '<': m -= 1
            if current.element != '@' and current.element != '$':
                current.element = 'x'
            current = self._retrieveElement(Index(n,m))

    def _defineWeight(self, element):
        return 2 if element == '%' else 1

    def _defineManhattanDistance(self, element):
        '''Recebe um Elemento'''
        n, m = element.index
        x = fabs(n-self._finalState.index.n)
        y = fabs(m-self._finalState.index.m)
        return x + y

    def _defineEuclidianDistance(self, element):
        '''Recebe um Elemento'''
        n, m = element.index
        x = fabs(n-self._finalState.index.n) ** 2
        y = fabs(m-self._finalState.index.m) ** 2
        return sqrt(x + y)

    def _processLabrinth(self):
        ''' O(n*m) '''
        processedLabrinth = []
        for n, line in enumerate(self._labrinth):
            currentLine = []
            for m, element in enumerate(line):
                currentElement = Element(element, Index(n, m), self._defineWeight(element))
                currentLine.append(currentElement)
                if element == '@':  self.estadoInicial = currentElement
                if element == '$':  self._finalState = currentElement
            processedLabrinth.append(currentLine)

        self._labrinth = processedLabrinth
        self.estadoInicial.weightOfLeastCostlyPath = 0

        if self._finalState is not None:
            for line in self._labrinth:
                for element in line:
                    element.distMan = self._defineManhattanDistance(element)
                    element.distEuc = self._defineEuclidianDistance(element)

    def _retrieveElement(self, index):
        ''' Recieves an Index (2-tuple named n,m) and returns a reference to a _labrinth Element. '''
        return self._labrinth[index.n][index.m]

    def _appendActions(self, new, current, move):
        '''
        Recieves two _labrinth elements: new, current.
        And a move, which is a one-char string of the following: '<','>','^','v'
        '''
        new.moves = current.moves[:]
        new.moves.append(move)

    def _lessCostlyPath(self, new):
        '''
        Recieves a candidate element. If the path being currently expanded is a less costly path than currently known, returns true. Otherwise, returns false.
        '''
        return self._costOfReachingLastExploredElement + new.weight < new.weightOfLeastCostlyPath

    def _updateWeights(self, new, current):
        new.weightOfLeastCostlyPath = current.weightOfLeastCostlyPath + new.weight

    def _appendToCandidates(self, element, candidates):
        candidates.append(element)

####################### Public functions ######################

    def expandir(self, current):
        ''' Recieves an Element object, with atributes of: element(one-char string), CHANGE(boolean), index(2-tuple named n,m) '''
        candidates = []
        n, m = current.index

        if current.visited:
            return []

        current.visited = True
        self._totalExpansions += 1
        self._costOfReachingLastExploredElement = current.weightOfLeastCostlyPath
        
        if current.element != '!' or current.element != '@' or current.element != '$':
            current.element = 'x'

        #Up ^
        if n-1 > -1:
            new = self._retrieveElement(Index(n-1, m))
            if self._permittedSpace(new) and self._lessCostlyPath(new):
                self._appendToCandidates(new, candidates)
                self._appendActions(new, current, '^')
                self._updateWeights(new, current)

        #Left >
        if m+1 < self._dimensions.m:
            new = self._retrieveElement(Index(n, m+1))
            if self._permittedSpace(new) and self._lessCostlyPath(new):
                self._appendToCandidates(new, candidates)
                self._appendActions(new, current, '>')
                self._updateWeights(new, current)

        #Down v
        if n+1 < self._dimensions.n:
            new = self._retrieveElement(Index(n+1, m))
            if self._permittedSpace(new) and self._lessCostlyPath(new):
                self._appendToCandidates(new, candidates)
                self._appendActions(new, current, 'v')
                self._updateWeights(new, current)

        #Right <
        if m-1 > -1:
            new = self._retrieveElement(Index(n, m-1))
            if self._permittedSpace(new) and self._lessCostlyPath(new):
                self._appendToCandidates(new, candidates)
                self._appendActions(new, current, '<')
                self._updateWeights(new, current)

        return candidates

    def ordenarPorCusto(self, a, b):
        return a.weightOfLeastCostlyPath < b.weightOfLeastCostlyPath

    def ordenarPorHeuristicaGulosa1(self, a, b):
        return a.distMan < b.distMan

    def ordenarPorHeuristicaGulosa2(self, a, b):
        return a.distEuc < b.distEuc

    def ordenarPorSoma1(self, a, b):
        return a.weightOfLeastCostlyPath + a.distMan < b.weightOfLeastCostlyPath + b.distMan

    def ordenarPorSoma2(self, a, b):
        return a.weightOfLeastCostlyPath + a.distEuc < b.weightOfLeastCostlyPath + b.distEuc

    def estadoFinal(self, current):
        if self._finalState is None:
            return True
        elif current.element == self._finalState.element:
            self._finalState.element = '!'
            self.solution = current.moves
            self._totalCostOfSolution = current.weightOfLeastCostlyPath
            self._nOfStepsInSolution = len(self.solution)
            self._implementSolution()
            return True
        return False

    def result(self):
        string = f"Total de expansões: {self._totalExpansions}\n" + \
                 f"Custo total: {self._totalCostOfSolution}\n" + \
                 f"Número de passos da solução: {self._nOfStepsInSolution}\n"
        return string

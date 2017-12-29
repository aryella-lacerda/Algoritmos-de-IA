from csp import csp
import copy
import queue

regions = (
        [['c'+str(i)+str(j) for i in range(0,9)] for j in range(0,9)] #colunas
        +[['c'+str(j)+str(i) for i in range(0,9)] for j in range(0,9)] #linhas
        +[['c'+str(i)+str(j) for i in range(3*y,3*y+3)for j in range(3*x, 3*x+3)] for x in range(0,3) for y in range(0,3)] #caixas
)

def readSudoku(file):
    def boxRange(x): return range((x//3)*3,(x//3)*3+3)
    def constraint(i,j): return (i != j)
    def arcgen(x,y): #gera uma lista das chaves que x, y restricoes
        return [
                'c'+str(i)+str(j) for i in range(0,9) for j in range(0,9)
                if(i != x or j != y) and (i == x or j == y or (i in boxRange(x) and j in boxRange(y)))
                ]

    data = [('c'+str(i)+str(j),c) for i, line in enumerate(open(file)) for j,c in enumerate(line[0:-1])]
    domains = {key:(list(range(1,10)) if c== '*' else [int(c)]) for (key,c) in data}
    arcs = {key: arcgen(int(key[1]),int(key[2])) for (key,c) in data}

    return csp(domains,arcs,constraint)

def printSudoku(csp):
    out = [list(range(0,9)) for i in range(0,9)]
    for x in csp.domains:
        out[int(x[1])][int(x[2])] = str(csp.domains[x][0]) if len(csp.domains[x]) == 1 else '*'
    for x in out:
        print(' '.join(x))


def removeInconsistent(csp,i,j):
    removed = False
    for x in csp.domains[i][:]:
        if not any([csp.constraint(x,y) for y in csp.domains[j]]):
            csp.domains[i].remove(x)
            removed = True
    return removed
def AC3(csp):
    q = [(i,j) for i in csp.domains for j in csp.arcs[i]]
    while q:
        i, j = q.pop()
        if removeInconsistent(csp,i,j):
            for k in csp.arcs[i]:
                if i != k:
                    q.append((k,i))

def solveForward(csp):
    changed = True
    AC3(csp)
    changed = False
    for r in regions: # para cada regiao (linha,coluna, caixa)
        domain = list(range(1,10))
        [domain.remove(csp.domains[k][0]) for k in r if len(csp.domains[k]) == 1]
        for d in domain: #iterar sobre os valores que não foram atribuído
            if sum(csp.domains[k].count(d) for k in r) == 1:
                csp.domains[[k for k in r if csp.domains[k].count(d)> 0][0]] = d # se apenas uma célula pode ter esse valor, atribua-a

def solveDFS(csp):
    q = queue.LifoQueue()
    q.put(copy.deepcopy(csp))
    while q:
        node = q.get()
        solveForward(node)
        if all([len(node.domains[k]) == 0 for k in node.domains]):
            return node #foi resolvido
        if not any([len(node.domains[k]) ==0 for k in node.domains]):
            guessKey = [k for k in node.domains if len(node.domains[k]) > 1][0]
            for guess in node.domains[guessKey]: #adiciona a lifo
                successor = copy.deepcopy(node)
                successor.domains[guessKey] = guess
                q.put(successor)

arq = readSudoku('tests/sudoku')
#removeInconsistent(arq,'c80','c08')
solve = solveDFS(arq)
#printSudoku(solve)

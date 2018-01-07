def constrainsViolated(Q):
    c = 0
    conflictsLine = []
    n = len(Q)
    for i in range(n):
        a = int(Q[i][0]) # pegando sempre o primeiro elemento de cada linha
        cl = 0 #conflitos por linha
        for j in range(n):
            b = int(Q[i][j])
            if a == b:
                c += 1
                cl += 1
            if (i - j == a - b) or (i - j == b - a):
                c += 1
                cl += 1

        conflictsLine.append(cl) #lista de conflitos por linha

    return c,conflictsLine # retorna o numero de conflitos total

def readFile():

    with open('queens.txt') as infile:
        # Read and Format Game Board
        dimensions = infile.readline().split(' ')
        nLines,nColumns = int(dimensions[0]),int(dimensions[1])
        lines = infile.readlines()
        gameBoard = []
        for line in lines:
            line = line.rstrip()
            if line != '':
                gameBoard.append(line.split(' '))


        print(gameBoard)
        nconflits, listNconflits = constrainsViolated(gameBoard)
        print(nconflits)

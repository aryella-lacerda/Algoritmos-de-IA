from queens import Queens

#teste antes de colocar na classe de queens.py
def attacks(column,i,j):
    if int(column[i]) == int(column[j]): return True
    if abs(i-j) == abs(int(column[i]) - int(column[j])): return True
    return False

#teste antes de colocar na classe de queens.py
def checkQueen(line):
    s = 0
    for i in line:
        s += int(i)
    return s

#teste antes de colocar na classe de queens.py
def constrainsViolated(Q):
    '''
        fazendo o J receber I consigo fazer a compraçao das colunas em O(n)
        o if do final é por que nunca era feita a comparacao do I = 0 e J = MAXSIZE
    '''
    for i in range(len(Q)):
        for j in range(i+1,len(Q)):
            if(attacks(Q[i],i,j)): #i -> coluna, j ->linha
                print('attacks')
        if i == len(Q)-1:
            if attacks(Q[0],i,len(Q)-1):

                print('attacks')
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

        #for line in gameBoard:
        #print(checkQueen(line))

        print(gameBoard)
        constrainsViolated(gameBoard)

readFile()

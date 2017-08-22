import cython
class state :
    def __init__(self,_currentState):
        self.currentState = _currentState
        self.childs = []
        self.move = ""
        self.utility=0
        self.type = ""
    def isTerminal(self):
        for i in self.currentState :
            for j in i :
                if j == "." :
                    return (False)
        return True
    def getChilds(self,turn):
        for i in range(len(self.currentState)):
            for j in range(len(self.currentState)):
                if self.currentState[i][j] == ".":
                    #Stake ---------------------------------------------
                    newState=  [row[:] for row in self.currentState]
                    newState[i][j] = turn
                    newBoard = state(newState)
                    newBoard.move = chr(j+65) + str(i+1) +" "+"Stake"
                    self.childs.append(newBoard)

                    #Raid ----------------------------------------------
        for i in range(len(self.currentState)):
            for j in range(len(self.currentState)):
                if self.currentState[i][j] == ".":
                    if (-1<i-1 and i-1<len(self.currentState) and -1<j and j<len(self.currentState))and self.currentState[i-1][j]== turn:
                        newState = [row[:] for row in self.currentState]
                        if self.raid(newState,i,j,turn):
                            newState[i][j] = turn
                            newBoard = state(newState)
                            newBoard.move = chr(j + 65) + str(i + 1) +" "+"Raid"
                            self.childs.append(newBoard)
                        else:
                            pass

                    if (-1<i+1 and i+1<len(self.currentState) and -1<j and j<len(self.currentState))and self.currentState[i+1][j]== turn:
                        newState =  [row[:] for row in self.currentState]
                        if self.raid(newState,i,j,turn):
                            newState[i][j] = turn
                            newBoard = state(newState)
                            newBoard.move = chr(j + 65) + str(i + 1) +" "+"Raid"
                            self.childs.append(newBoard)
                        else:
                            pass

                    if (-1<i and i<len(self.currentState) and -1<j-1 and j-1<len(self.currentState)) and self.currentState[i][j-1]== turn:
                        newState =  [row[:] for row in self.currentState]
                        if self.raid(newState,i,j,turn):
                            newState[i][j] = turn
                            newBoard = state(newState)
                            newBoard.move = chr(j + 65) + str(i + 1) +" "+"Raid"
                            self.childs.append(newBoard)
                        else:
                            pass

                    if (-1<i and i<len(self.currentState) and -1<j+1 and j+1<len(self.currentState)) and self.currentState[i][j+1]== turn:
                        newState =  [row[:] for row in self.currentState]
                        if self.raid(newState, i, j,turn) :
                            newState[i][j] = turn
                            newBoard = state(newState)
                            newBoard.move = chr(j + 65) + str(i + 1) +" "+"Raid"
                            self.childs.append(newBoard)
                        else:
                            pass
        return self.childs
    def raid(self,pos,i,j,turn):
        count = 0
        if (-1<i-1 and i-1<len(pos) and -1<j and j<len(pos)) and pos[i-1][j] != "." and pos[i-1][j] != turn  :
            pos[i-1][j] = turn
            count +=1
        if (-1<i+1 and i+1<len(pos) and -1<j and j<len(pos)) and pos[i+1][j] != "." and pos[i+1][j] != turn :
            pos[i+1][j] = turn
            count += 1
        if (-1<i and i<len(pos) and -1<j-1 and j-1<len(pos)) and pos[i][j-1] != "." and pos[i][j-1] != turn :
            pos[i][j-1] = turn
            count += 1
        if (-1<i and i<len(pos) and -1<j+1 and j+1<len(pos)) and pos[i][j+1] != "." and pos[i][j+1] != turn :
            pos[i][j+1] = turn
            count += 1
        if count == 0 :
            return False
        else:
            return True

def getUtility(state,score,player):
    score1 = 0
    score2 = 0
    for i in range(len(score)):
        for j in range(len(score)):
            if state[i][j] == player:
                score1 += score[i][j]
            if state[i][j]!=player and state[i][j]!= ".":
                score2 += score[i][j]
    return (score1 - score2)



def minimax(startState, score ,firstdephtLimit,firstTurn):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Fig. 6.4]"""
    def max_value(state,dephtLimit):
        if state.isTerminal() or dephtLimit==0:
            return getUtility(state.currentState,score,firstTurn)
        v = -1000000
        t = None
        if firstTurn == "O":
            t = "O"
        else:
            t = "X"
        for c in state.getChilds(t):

            v = max(v, min_value(c,dephtLimit-1))
        return v

    def min_value(state,dephtLimit):
        if state.isTerminal() or dephtLimit==0:
            return getUtility(state.currentState,score,firstTurn)
        v = 1000000
        t = None
        if firstTurn == "O":
            t = "X"
        else:
            t = "O"
        for c in state.getChilds(t):

            v = min(v, max_value(c,dephtLimit-1))
        return v


    bestScore = -10000000
    bestAction = None
    bestState = None
    for c in startState.getChilds(firstTurn):
        c.utility = getUtility(c.currentState, score, firstTurn)
        c.type = "min"

        v = min_value(c,firstdephtLimit)
        if v > bestScore :
            bestScore = v
            bestAction = c.move
            bestState = c.currentState

    return [bestAction,bestState]

def alphabeta(startState, score,firstDephtlimit,firstTurn):

    def max_value(state,dephtLimit, alpha, beta):
        if state.isTerminal() or dephtLimit==0:
            return getUtility(state.currentState, score, firstTurn)
        v = -1000000
        if firstTurn == "O":
            t = "O"
        else:
            t = "X"
        for c in state.getChilds(t):
            v = max(v, min_value(c,dephtLimit-1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state,dephtLimit, alpha, beta):
        if state.isTerminal() or dephtLimit == 0:
            return getUtility(state.currentState, score, firstTurn)
        v = 1000000
        if firstTurn == "O":
            t = "X"
        else:
            t = "O"
        for c in state.getChilds(t):
            v = min(v, max_value(c,dephtLimit-1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


    best_score = -1000000
    beta = 1000000
    best_action = None
    best_state = None
    for c in startState.getChilds(firstTurn):
        v = min_value(c, firstDephtlimit,best_score,beta)
        if v>best_score :
            best_score = v
            best_action = c.move
            best_state = c.currentState
    return [best_action,best_state]

f = open("input.txt")
boardSize = int(f.readline()[0])
mode = f.readline()
youplay = f.readline()[0]
depht = int(f.readline()[0])
boardScores = []
for line in range(boardSize):
    tmp = f.readline().split()
    row = []
    for i in tmp :
        row.append(int(i))
    boardScores.append(row)

boardTer = []
for line in range(boardSize):
    row = []
    tmp = f.readline()
    for i in range(boardSize):
        row.append(tmp[i])
    boardTer.append(row)

start = state(boardTer)
result = None
if mode.startswith("MINIMAX") :
    result = minimax(start,boardScores,depht-1,youplay)
elif mode.startswith("ALPHABETA"):
    result = alphabeta(start, boardScores,depht-1,youplay)
#print(result)
o = open("output.txt","w")
o.write(result[0])
o.write("\n")
for i in result[1]:
    tmp = ""
    for j in i:
        tmp+= str(j)
    o.write(tmp)
    o.write("\n")

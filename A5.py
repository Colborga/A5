import operator
from random import randint

import numpy

state = [[1, 2, 3], [], []]
goalState = [[], [], [1, 2, 3]]

Q = {}

def printState(state):
    row = ""
    for i in range(3):
        for peg in state:
            if len(peg) > i:
                row += str(peg[i])
                row += "   "
        print(row)
        row = ""

def randomState():

    diskOneIndex = randint(0, 2)
    diskTwoIndex = randint(0, 2)
    diskThreeIndex = randint(0, 2)

    global state
    state = [[], [], []]
    state[diskOneIndex].append(1)
    state[diskTwoIndex].append(2)
    state[diskThreeIndex].append(3)



def validMoves(state):
    moves = []

    pegIndex = 0
    for peg in state:
        pegIndex += 1
        for peg2 in range(len(state)):
            if peg is not peg2:
                topDisk = next(iter(peg or []), None)
                if topDisk is not None:
                    topDiskDesPeg = next(iter(state[peg2] or []), None)

                    if topDiskDesPeg is not None:
                        if topDisk < topDiskDesPeg:
                            moves.append([pegIndex, peg2 + 1])
                    else:
                        moves.append([pegIndex, peg2 + 1])

    return moves

def makeMove(state, move):
    if validMoves(state).__contains__(move):
        #Make the move
        topDisk = next(iter(state[move[0] - 1] or []), None)
        if topDisk is not None:
            state[move[0] - 1].remove(topDisk)
            state[move[1] - 1].insert(0, topDisk)
        return state

    return state

def trainQ(nRepetitions, learningRate, epsilonDecayFactor, validMovesF, makeMoveF):
    global state
    global Q

    for puzzleCompletion in range(nRepetitions):
        goalReached = False

        oldKey = None
        previousState = None
        currentKey = None

        epsilonDecayFactor = epsilonDecayFactor
        randomState()

        numMoves = 0
        while goalReached is False:
            moves = validMovesF(state)
            numMoves += 1

            if moves is not None:
                # ###################################Get the next Move####################################
                # randInt is not inclusive...
                if randint(0, 101) / 100 < epsilonDecayFactor ** puzzleCompletion:
                    nextMove = moves[randint(0, len(moves) - 1)]
                    #print("Rand")
                else:
                    if previousState:
                        minValue = 1000000
                        for eachMove in moves:
                            loopKey = (str(state), str(eachMove))
                            if loopKey not in Q.keys():
                                # move is not in the dictionary, add with -1 value
                                Q[loopKey] = -1

                            if Q[loopKey] < minValue:
                                # found new minimum value
                                minValue = Q[loopKey]

                                # this is the move that will get the minimum value
                                nextMove = eachMove
                                # New state/move combo, insert into dict with -1
                    else:
                        # previous state is None, set to a random move
                        nextMove = moves[randint(0, len(moves) - 1)]
                ##########################################################################################

                currentKey = (str(state), str(nextMove))
                if currentKey not in Q.keys():
                    Q[currentKey] = -1

                # print(state)
                if state == goalState:
                    goalReached = True

                    if oldKey in Q.keys():
                        Q[oldKey] = Q[oldKey] + learningRate * (1 - Q[oldKey])
                    else:
                        Q[oldKey] = -1

                else:
                    if previousState:
                        if oldKey in Q.keys():
                            Q[oldKey] = Q[oldKey] + learningRate * (1 + Q[currentKey] - Q[oldKey])
                        else:
                            Q[oldKey] = -1

                    oldKey = currentKey
                    previousState = state
                    state = makeMoveF(state, nextMove)
    return Q, list(Q.values())

def testQ(Q, maxSteps, validMovesF, makeMoveF):
    global state



    for i in range(maxSteps):
        minValue = 1000
        nextMove = None

        moves = validMovesF(state)
        for eachMove in moves:
            loopKey = (str(state), str(eachMove))

            if loopKey in Q.keys():
                if Q[loopKey] < minValue:
                    # found new minimum value
                    minValue = Q[loopKey]

                    nextMove = eachMove
        state = makeMoveF(state, nextMove)

        if state == goalState:
            return state
    return state

if __name__ == "__main__":
    # printState(state)
    # print(validMoves([[1, 2, 3], [], []]))

    print(trainQ(500, .5, .7, validMoves, makeMove))

    state = [[1, 2, 3], [], []]
    print(testQ(Q, 250, validMoves, makeMove))

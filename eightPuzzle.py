import time
import random
import copy

pMatrixEasy = [
    [1,2,3],   # easy for matrix A
    [4,5,6],
    [7,8,0]
]

pMatrixHard = [
    [3,5,8],
    [4,7,6],
    [2,1,0]
]

pMatrix = [
    [3,5,8],
    [4,7,6],
    [2,1,0]

    # [1,2,3],   # easy for matrix A
    # [4,5,6],
    # [7,8,0]

    # [4,8,0],   # hard for matrix A
    # [6,1,3],
    # [2,5,7]

    # [2,8,3], # easy for matrix B
    # [1,6,4],
    # [7,0,5]

]

pGoalMatrix = [
    [1,2,3],    # matrix A
    [4,5,6],
    [7,8,0]

    # [1,2,3],  # matrix B
    # [8,0,4],
    # [7,6,5]
]

def index(item, seq):  # find the index of item in matrix
    if item in seq:
        return seq.index(item)
    else:
        return -1

def indexListMatrix(matrix):  # indexing the i, j in goal matrix
    indexList = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            indexList[matrix[i][j]] = (i,j)
    return indexList  

def listOfMovement(iLength, jLength, point, pointPrev):
    listMove = {
        'up': 1,
        'right': 1,
        'down': 1,
        'left': 1
    }

    if point[0] == iLength - 1:
        listMove['down'] = 0
    elif point[0] == 0:
        listMove['up'] = 0

    if point[1] == jLength - 1:
        listMove['right'] = 0
    elif point[1] == 0:
        listMove['left'] = 0

    if pointPrev == 'left':
        listMove['right'] = 0
    elif pointPrev == 'right':
        listMove['left'] = 0
    elif pointPrev == 'up':
        listMove['down'] = 0
    elif pointPrev == 'down':
        listMove['up'] = 0

    return listMove


class whiteCell:
    def __init__(self, pointNow, pointPreValue):
        self.pointNow = pointNow
        self.pointPreValue = pointPreValue

    def __str__(self):
        string = 'Point Now: ' + '(' + str(self.pointNow.i) + ', ' + str(self.pointNow.j) + ')'
        return string

def autoFindWhiteCell(matrix):
    for i in  range(len(matrix)):
        if 0 in matrix[i]:
            return whiteCell((i, matrix[i].index(0)), '')

def copyObj(obj):
    newMatrix= []
    for i in obj.matrix:
        newMatrix.append(i[:])
    pointNow = obj.whiteCell.pointNow
    pointPreValue = obj.whiteCell.pointPreValue
    white = whiteCell(pointNow, pointPreValue)
    parent = obj.parent
    depth = obj.depth
    hVal = obj.hVal
    return matrixObj(newMatrix, white, parent, depth, hVal)

class matrixObj:
    def __init__(self, matrix, whiteCell=0, parent=None, depth=0, hVal=0):
        self.matrix = matrix
        if whiteCell == 0:
            self.whiteCell = autoFindWhiteCell(self.matrix)
        else:
            self.whiteCell = whiteCell            
        self.parent = parent
        self.depth = depth
        self.hVal = hVal
        
    def __str__(self):
        string = ''
        for i in range(len(self.matrix)):            
            for j in range(len(self.matrix[i])):
                if(self.matrix[i][j]):
                    string = string + str(self.matrix[i][j]) +  ' '
                else: string = string + ' ' + ' '
            string += '\n'
        return string

    def shuffle(self, numberShuffle):        
        for i in range(numberShuffle):            
            List = self.generatePattern()
            self = random.choice(List)
        return self


    def moveUp(self, point):
        matrix = self.matrix        
        i, j = point[0], point[1]
        matrix[i - 1][j], matrix[i][j] = matrix[i][j], matrix[i - 1][j]

    def moveDown(self, point):
        matrix = self.matrix        
        i, j = point[0], point[1]
        matrix[i + 1][j], matrix[i][j] = matrix[i][j], matrix[i + 1][j]

    def moveLeft(self,point):
        matrix = self.matrix        
        i, j = point[0], point[1]
        matrix[i][j - 1], matrix[i][j] = matrix[i][j], matrix[i][j - 1]

    def moveRight(self, point):
        matrix = self.matrix        
        i, j = point[0], point[1]
        matrix[i][j + 1], matrix[i][j] = matrix[i][j], matrix[i][j + 1]

    def mismatchNumber(self, indexMatrix):  # heuristic mahattan
        count = 0
        for i in range(3):    # len of matrix elements
            for j in range(3): # len of matrix[i] elements
                xy = indexMatrix[self.matrix[i][j]]
                count = count + abs(xy[0] - i) + abs(xy[1] - j)
        return count


    def generatePattern(self):
        listMove = listOfMovement(len(self.matrix), len(self.matrix[0]), self.whiteCell.pointNow, self.whiteCell.pointPreValue);
        listGenerate = []
        pointNow = self.whiteCell.pointNow

        if listMove['left']:    # accelerate speed up 1.0s
            newMatrix = copyObj(self)
            newMatrix.moveLeft(pointNow)
            newMatrix.whiteCell.pointPreValue = 'left'
            newMatrix.whiteCell.pointNow = (newMatrix.whiteCell.pointNow[0], newMatrix.whiteCell.pointNow[1] - 1)
            listGenerate.append(newMatrix)

        if listMove['right']:
            newMatrix = copyObj(self)
            newMatrix.moveRight(pointNow)
            newMatrix.whiteCell.pointPreValue = 'right'
            newMatrix.whiteCell.pointNow = (newMatrix.whiteCell.pointNow[0], newMatrix.whiteCell.pointNow[1] + 1)
            listGenerate.append(newMatrix)

        if listMove['up']:
            newMatrix = copyObj(self)
            newMatrix.moveUp(pointNow)
            newMatrix.whiteCell.pointPreValue = 'up'
            newMatrix.whiteCell.pointNow = (newMatrix.whiteCell.pointNow[0] - 1, newMatrix.whiteCell.pointNow[1])
            listGenerate.append(newMatrix)

        if listMove['down']:
            newMatrix = copyObj(self)
            newMatrix.moveDown(pointNow)
            newMatrix.whiteCell.pointPreValue = 'down'
            newMatrix.whiteCell.pointNow = (newMatrix.whiteCell.pointNow[0] + 1, newMatrix.whiteCell.pointNow[1])
            listGenerate.append(newMatrix)

        return listGenerate  

def traceRoute(p):  # print matrix step by step
    if p.parent == None:
        return p
    else:
        print traceRoute(p.parent)
        return p

def traceDirection(p, listDirection):  # print list of movement step by step
    if p.parent == None:               # we read listDirection from end to begin of list
        return p
    else:
        listDirection.append({
            'direction': p.whiteCell.pointPreValue,
            'number': p.parent.matrix[p.whiteCell.pointNow[0]][p.whiteCell.pointNow[1]]
        })
        pattern =  traceDirection(p.parent, listDirection)
        return p

def isMatched(p, pGoal):
    return p.matrix == pGoal.matrix

def puzzle(p, pGoal, indexMatrix):
    Open = [p]
    Close = []
#    Open.append(p)

    while(Open):
        current = Open.pop(0)
        if isMatched(current, pGoal):
            print 'finally goal'
            return current

        List = current.generatePattern()  # accelerate speed up 0.5s

        for subP in List:
            hVal = subP.mismatchNumber(indexMatrix)
            fVal = current.depth + 1 + hVal

            indexOpen = index(subP, Open)
            indexClose = index(subP, Close)

            if indexOpen == -1 and indexClose == -1:
                # new member
                subP.parent = current
                subP.depth = current.depth + 1
                subP.hVal = hVal
                Open.append(subP)

            elif indexOpen > -1:
                # subP similar parent's neighbour
                neighbour = Open[indexOpen]
                if fVal < neighbour.hVal + neib.depth:
                    neighbour.parent = current
                    neighbour.depth = current.depth + 1
                    neighbour.hVal = hVal

            elif indexClose > -1:
                neighbour = Close[indexClose]                
                if fVal < neighbour.hVal + neib.depth:
                    subP.parent = current
                    subP.depth = current.depth + 1
                    subP.hVal = hVal
                    Close.remove(indexOpen)
                    Open.append(subP)



        Close.append(current)  
        Open = sorted(Open, key=lambda obj: obj.hVal + obj.depth)


def mainEightPuzzle(currentMatrix):
    p = matrixObj(currentMatrix)
    pGoal = matrixObj(pGoalMatrix)
    indexMatrix = indexListMatrix(pGoal.matrix)

    listDirection = []
    pSolved = puzzle(p, pGoal, indexMatrix)

    traceDirection(pSolved, listDirection)
    return listDirection

def shuffleEightPuzzle(dificulty, numberShuffle):
    if dificulty == 'easy':
        p = matrixObj(pMatrixEasy)
        return p.shuffle(numberShuffle).matrix

    elif dificulty == 'hard':
        p = matrixObj(pMatrixHard)
        return p.shuffle(numberShuffle).matrix

    p = matrixObj(pMatrix)
    return p.matrix
#    return p.shuffle(numberShuffle).matrix




def convertMatrixIntoList(matrix):
    List = []
    for iMatrix in matrix:
        for j in iMatrix:
            List.append(j)
    return List

#shuffleEightPuzzle(10)

# p = [
#     [2,8,3],
#     [1,6,4],
#     [7,0,5]
# ]

# pGoal = [
#     [1,2,3],
#     [8,0,4],
#     [7,6,5]
# ]

# print mainEightPuzzle(p, pGoal)



# =================================================================
# test shuffle
# print shuffleEightPuzzle(10)


# =================================================================

# Just test the module
# p = matrixObj([

    # [4,8,0],
    # [6,1,3],
    # [2,5,7]

#     # [4,3,5],
#     # [2,7,8],
#     # [1,0,6]

#     # [1,2,3],
#     # [5,7,6],
#     # [4,0,8]

#     # [2,8,3],
#     # [1,6,4],
#     # [7,0,5]
# ])

# pGoal = matrixObj([
#     [1,2,3],
#     [4,5,6],
#     [7,8,0]
# ])

# # print traceRoute(puzzle(p, pGoal))

# listDirection = []
# traceDirection(puzzle(p, pGoal), listDirection)
# print listDirection

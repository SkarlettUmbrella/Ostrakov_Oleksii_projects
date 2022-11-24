# Ostrakov Oleksii, UI zad1.d
# My program uses greedy algorithms with heuristics 1 and 2
#
# number [1:inf) = number of a square
# number 0 = empty square
# NODES: class Matrix()
# OPERATORS: UP, DOWN, LEFT, RIGHT
# STATE: list Matrix.nodes = []
# HEURISTIC 1: mark all squares that are not on target location
# HEURISTIC 2: summary of all distances of all squares to their target locations

import copy
import timeit

# !!! DANGER !!!
# !!! INCREASING RECURSION LIMIT !!!
# import sys
# print(sys.setrecursionlimit(2000))

# class to store nodes
class Matrix:
    globalM = 0
    # global number of columns of matrix
    globalN = 0
    # global number of rows of matrix
    globalLen = 0
    # M * N.

    # create empty matrix
    def __init__(self):
        self.nodes = []

    # fill matrix with array
    def fill(self, array):
        for i in array:
            self.nodes.append(i)

# main class of program
class globalVar:
    wayArray = []
    # correct path of puzzle
    usedArray = []
    # all occurred nodes of puzzle
    wayFound = 0
    # switch path is found
    details = ''
    # switch for turning on additional output
    algo = ''
    # switch for heuristics

    # main preparation for program
    def __init__(self, startMatrix, endMatrix):
        self.startMatrix = startMatrix
        self.endMatrix = endMatrix
        self.wayArray.append(startMatrix)
        self.usedArray.append(hash(startingMatrix))

    # check if currentMatrix was never used before
    def uniqueMatrix(self, currentMatrix):
        if endMatrix.nodes == currentMatrix.nodes:
            self.wayFound = 1
            return 1
        for i in self.usedArray:
            if i == hash(currentMatrix):
                return -1
        return 0

    # main recursive function to find a path
    def checkWays(self, currentMatrix, lastWay):
        # find 0 in node, then find directions where puzzle can go
        emptySpaceLocation = currentMatrix.nodes.index(0)
        allDirections = []
        if emptySpaceLocation < (Matrix.globalLen - Matrix.globalM) and lastWay != "DOWN":
            upMatrix = self.swapUp(currentMatrix)
            if self.wayFound == 1:
                return
            if upMatrix is not None:
                upDirection = [self.algoAuto(upMatrix), upMatrix, "UP"]
                allDirections.append(upDirection)

        if emptySpaceLocation >= Matrix.globalM and lastWay != "UP":
            downMatrix = self.swapDown(currentMatrix)
            if self.wayFound == 1:
                return
            if downMatrix is not None:
                downDirection = [self.algoAuto(downMatrix), downMatrix, "DOWN"]
                allDirections.append(downDirection)

        if emptySpaceLocation % Matrix.globalM != 0 and lastWay != "LEFT":
            rightMatrix = self.swapRight(currentMatrix)
            if self.wayFound == 1:
                return
            if rightMatrix is not None:
                rightDirection = [self.algoAuto(rightMatrix), rightMatrix, "RIGHT"]
                allDirections.append(rightDirection)

        if (emptySpaceLocation + 1) % Matrix.globalM != 0 and lastWay != "RIGHT":
            leftMatrix = self.swapLeft(currentMatrix)
            if self.wayFound == 1:
                return
            if leftMatrix is not None:
                leftDirection = [self.algoAuto(leftMatrix), leftMatrix, "LEFT"]
                allDirections.append(leftDirection)

        # only possible direction now in allDirections
        allDirections.sort(key=lambda x: int(x[0]))

        if self.details == 'y':
            print("current matrix: ", end=" ")
            for j in currentMatrix.nodes:
                print(j, end=" ")
            print()
            print("avaliable paths: ")
            for i in allDirections:
                print(i[0], ": ", end=" ")
                for j in i[1].nodes:
                    print(j, end=" ")
                print()

        # for all possible direction go recursively
        for i in allDirections:
            if self.wayFound != 1 and self.uniqueMatrix(i[1]) == 0:
                # hash node as once occurred
                self.usedArray.append(hash(i[1]))
                # add node temporarily as correct in final order
                self.wayArray.append(i[1])
                try:
                    if self.details == 'y':
                        print("chosen: ", i[0], ", array: ", end=" ")
                        for j in i[1].nodes:
                            print(j, end=" ")
                        print()
                        print()
                    # recursive call of itself, i[1] is next Matrix(next node), i[2] is last used direction
                    self.checkWays(i[1], i[2])
                except RecursionError:
                    print("RECURSION ERROR")
                    self.wayArray.remove(currentMatrix)
                    self.usedArray.clear()
                    for i in self.wayArray:
                        self.usedArray.append(hash(i))
                    return
                if self.details == 'y':
                    print("returning to previous one.")
        # remove node if not in final(correct) order
        if self.wayFound != 1:
            self.wayArray.remove(currentMatrix)

    # move piece to left
    def swapLeft(self, oldMatrix):
        newMatrix = copy.deepcopy(oldMatrix)
        zeroPos = newMatrix.nodes.index(0)
        swapPos = zeroPos + 1
        swap = newMatrix.nodes[swapPos]
        newMatrix.nodes.remove(0)
        newMatrix.nodes.insert(swapPos, 0)
        # check if new node is unique
        unique = self.uniqueMatrix(newMatrix)
        if unique == -1:
            return None
        if unique == 1:
            self.wayArray.append(newMatrix)
            self.usedArray.append(hash(newMatrix))
            return
        return newMatrix

    # move piece to right
    def swapRight(self, oldMatrix):
        newMatrix = copy.deepcopy(oldMatrix)
        zeroPos = newMatrix.nodes.index(0)
        swapPos = zeroPos - 1
        swap = newMatrix.nodes[swapPos]
        newMatrix.nodes.remove(0)
        newMatrix.nodes.insert(swapPos, 0)
        # check if new node is unique
        unique = self.uniqueMatrix(newMatrix)
        if unique == -1:
            return None
        if unique == 1:
            self.wayArray.append(newMatrix)
            self.usedArray.append(hash(newMatrix))
            return
        return newMatrix

    # move piece up
    def swapUp(self, oldMatrix):
        newMatrix = copy.deepcopy(oldMatrix)
        zeroPos = newMatrix.nodes.index(0)
        swapPos = zeroPos + Matrix.globalM
        swap = newMatrix.nodes[swapPos]
        newMatrix.nodes.remove(0)
        newMatrix.nodes.remove(swap)
        newMatrix.nodes.insert(zeroPos, swap)
        newMatrix.nodes.insert(swapPos, 0)
        # check if new node is unique
        unique = self.uniqueMatrix(newMatrix)
        if unique == -1:
            return None
        if unique == 1:
            self.wayArray.append(newMatrix)
            self.usedArray.append(hash(newMatrix))
            return
        return newMatrix

    # move piece down
    def swapDown(self, oldMatrix):
        newMatrix = copy.deepcopy(oldMatrix)
        zeroPos = newMatrix.nodes.index(0)
        swapPos = zeroPos - Matrix.globalM
        swap = newMatrix.nodes[swapPos]
        newMatrix.nodes.remove(0)
        newMatrix.nodes.remove(swap)
        newMatrix.nodes.insert(swapPos, 0)
        newMatrix.nodes.insert(zeroPos, swap)
        # check if new node is unique
        unique = self.uniqueMatrix(newMatrix)
        if unique == -1:
            return None
        if unique == 1:
            self.wayArray.append(newMatrix)
            self.usedArray.append(hash(newMatrix))
            return
        return newMatrix

    # print all nodes in order to achieve target node
    def printSolution(self):
        for currentMatrix in self.wayArray:
            for i in currentMatrix.nodes:
                print(i, end=" ")
            print()

    # print all directions in order to achieve target node
    def printRoute(self):
        wayMoves = []
        for i in range(len(self.wayArray) - 1):
            zero = self.wayArray[i].nodes.index(0)
            next = self.wayArray[i + 1].nodes.index(0)
            if zero - next == 1:
                wayMoves.append("RIGHT")
            elif zero - next == -1:
                wayMoves.append("LEFT")
            elif zero - next == Matrix.globalM:
                wayMoves.append("DOWN")
            elif zero - next == -(Matrix.globalM):
                wayMoves.append("UP")
            else:
                print("Error")
                return
        for i in wayMoves:
            print(i)

    # choose heuristic to work with
    def algoAuto(self, currentMatrix):
        if self.algo == "1":
            return self.algo1(currentMatrix)
        elif self.algo == "2":
            return self.algo2(currentMatrix)

    # heuristic 1
    def algo1(self, currentMatrix):
        heuristic = 0
        for i in currentMatrix.nodes:
            if i != self.endMatrix.nodes[currentMatrix.nodes.index(i)]:
                heuristic += 1
        return heuristic

    # heuristic 2
    def algo2(self, currentMatrix):
        heuristic = 0
        for i in currentMatrix.nodes:
            if i != 0:
                a = currentMatrix.nodes.index(i)
                b = self.endMatrix.nodes.index(i)
                c = abs(a // Matrix.globalM - b // Matrix.globalM) + abs(a % Matrix.globalM - b % Matrix.globalM)
                heuristic += c
        return heuristic


if __name__ == '__main__':

    inputArr = input("define matrix size: ").split()
    if len(inputArr) != 2:
        print("only need 2 numbers!")
        quit()
    inputArr[0] = int(inputArr[0])
    inputArr[1] = int(inputArr[1])

    # define main variables
    matrixLen = inputArr[0] * inputArr[1]
    Matrix.globalM = int(inputArr[0])
    Matrix.globalN = int(inputArr[1])
    Matrix.globalLen = matrixLen
    startingMatrix = Matrix()
    endMatrix = Matrix()
    print()
    inputArr.clear()

    # fill start nodes from input
    inputArr = input('define starting matrix: ').split()
    if len(inputArr) != matrixLen:
        print("wrong amount of numbers!")
        quit()
    for i in inputArr:
        startingMatrix.nodes.append(int(i))
    print()
    inputArr.clear()

    # fill target nodes from input
    inputArr = input('define target matrix: ').split()
    if len(inputArr) != matrixLen:
        print("wrong amount of numbers!")
        quit()
    for i in inputArr:
        endMatrix.nodes.append(int(i))
    print()

    globalVar = globalVar(startingMatrix, endMatrix)

    # choose heuristic
    globalVar.algo = input("choose heuristic(1. or 2.): ")

    # choose to do additional output
    globalVar.details = input("Show additional details?(y/n): ")
    print()

    #start recursive search
    start = timeit.default_timer()
    globalVar.checkWays(startingMatrix, None)
    stop = timeit.default_timer()

    # print results
    print('result:')
    globalVar.printSolution()
    globalVar.printRoute()

    print()
    print("Search was completed in: ", (stop - start), " seconds.")
    print("Amount of unique nodes: ", len(globalVar.usedArray))
    print("Amount of steps in corrent route: ", len(globalVar.wayArray) - 1)

    print()

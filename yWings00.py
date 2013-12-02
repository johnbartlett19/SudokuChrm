#/bin/python

def findTwos(cellSet):
    returnSet = []
    for cell in cellSet:
        if cell.countHints() == 2:
            returnSet.append(cell)
    return returnSet

def findTwosSet(cellSet, hintSet):
    returnSet = []
    for cell in cellSet:
        for x in range(9):
            if cell.hints[x] and x in hintSet and cell not in returnSet:
                returnSet.append(cell)
    return returnSet

def findVisibleCells(cell, cellSet):
    returnSet = []
    for vCell in cellSet:
        if vCell.row == cell.row or vCell.col == cell.col or vCell.sqr == cell.sqr:
            if vCell != cell:
                returnSet.append(vCell)
    return returnSet

def findCommonCells(cellSet1, cellSet2):
    returnSet = []
    for cell in cellSet1:
        if cell in cellSet2:
            returnSet.append(cell)
    return returnSet

def findYwingPairs(c1hints, cellSet):
    ''' look in cellSet, find pairs of cells with a common hint that is not one of the
         true hints in the original cell'''
    returnSet = []
    hintCount = [0 for x in range(9)]  #count the hints of each type in this cell set
    for dCell in cellSet:
        for hint in range(9):
            if dCell.hints[hint] and hint not in c1hints:
                hintCount[hint] += 1
    for x in range(9):  # find pairs with hint not in original cell
        if hintCount[x] == 2:
            pair = []
            for cell in cellSet:
                if cell.hints[x]:
                    pair.append(cell)
            returnSet.append((pair,x))
    return returnSet

def findYwingSet(cell, cellSet):
    ''' we assume here that cellSet is visible, and only has two hints true '''
    c1hints = []  # get true hints in starter cell
    for x in range(9):
        if cell.hints[x]:
            c1hints.append(x)
    twoHintCells = []
    for cCell in cellSet:  # find cells with at least one hint in common
        for hint in c1hints:
            if cCell.hints[hint]:
                if cCell not in twoHintCells:
                    twoHintCells.append(cCell)
    ''' look in cellSet, find pairs of cells with a common hint that is not one of the
         true hints in the original cell'''
    returnSet = []
    hintCount = [0 for x in range(9)]  #count the hints of each type in this cell set
    for dCell in twoHintCells:
        for hint in range(9):
            if dCell.hints[hint] and hint not in c1hints:
                hintCount[hint] += 1

    for x in range(9):  # find pairs with hint not in original cell
        if hintCount[x] == 2:
            pair = []
            for cellT in twoHintCells:
                if cellT.hints[x]:
                    pair.append(cellT)
            otherHint = []
            for cellP in pair:
                for y in range(9):
                    if cellP.hints[y] and y != x:
                        otherHint.append(y)
            if otherHint[0] != otherHint[1] and otherHint[0] in c1hints and otherHint[1] in c1hints:
                returnSet.append((pair,x))
    return (returnSet)

def solveYwings(game):
    change = False
    for cell in game['Cells']:
        if cell.countHints() == 2:
            aa = findVisibleCells(cell, game['Cells'])
            bb = findTwos(aa)
            pairSet = findYwingSet(cell,bb)
            if len(pairSet) > 0:
                print 'Found yWing',cell, pairSet
                for (pair, hint) in pairSet:
                    common = findCommonCells(findVisibleCells(pair[0],game['Cells']),findVisibleCells(pair[1],game['Cells']))
                    for cellF in common:
                        if cellF != cell and cellF.hints[hint]:
                            cellF.hints[hint] = False
                            print 'Clearing hint', hint, 'in', cellF
                            return True
    return False























                

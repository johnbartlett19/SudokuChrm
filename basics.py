
#/bin/python
from classes import *

def countHintGroup(cellArray):
    ''' count the number of hints set in a set of cells, return 9 digit result in array '''
    mask = [0 for x in range(9)]
    for cell in cellArray:
        for x in range(9):
            if cell.hints[x]:
                mask[x] += 1
    return mask
                
def setGameStart(game, inString):
    for cell in game.cells:
        cellNum = 9 * (cell.row) + (cell.col)
        if inString[cellNum] != '0' and inString[cellNum] != ' ':
            cell.setAnswer(int(inString[cellNum])-1)

#def solveNakedSets(game):
#    for setSize in range(2,5):
#        print 'Checking for naked sets size', setSize
#        groupSet = ['Rows', 'Cols', 'Squares']
#        for group in groupSet:
#            for seg in game[group]:
#                if seg.solveNakedSets(setSize):
#                    return True
#    return False

#def solveHiddenSets(game):
#    for setSize in range(2,5):
#        print 'Checking for hidden sets size ', setSize
#        groupSet = ['Rows', 'Cols', 'Squares']
#        for group in groupSet:
#            for seg in game[group]:
#                if seg.solveHiddenSets(setSize):
#                    return True
#    return False

def solvePointingPairs(game):
    for square in game['Squares']:
        found = square.findPairs(square.cells)
        print found
    return False
            
def inputPuzzle():
    inArray = ["'"]
    for x in range(9):
        inArray.append(raw_input('Nine characters of line ' + str(x+1) + ': '))
    inArray.append("'")
    outStr = ''
    for part in inArray:
        outStr = outStr + part
    print 'inString = ' + outStr

#def solvePointingSets(game):
#    print 'Checking for pointing sets'
#    change = False
#    aa = game['Squares']
#    change = False
#    for square in aa:
#        pairSets = square.findPointingPair()
#        for row,col,sqr,cells,hint in pairSets:
#            if row != None:
#                change = game['Rows'][row].clearPtPairHints(cells, hint) or change
#            elif col != None:
#                change = game['Cols'][col].clearPtPairHints(cells, hint) or change
#    return change

#def boxLineReduction(game):
#    print 'Checking box line reductions'
#    change = False
#    aa = game['Rows'] + game['Cols']
#    change = False
#    for seg in aa:
#        pairSets = seg.findPointingPair()
#        for row,col,sqr, cells,hint in pairSets:
#            change = game['Squares'][sqr].clearPtPairHints(cells, hint) or change
#    return change

def checkGame(game):
    good = True
    sets = ['Rows', 'Cols', 'Squares']
    for set in sets:
        for seg in game[set]:
            ans = [0 for x in range(9)]
            for x in range(9):
                cell = seg.cells[x]
                if cell.answer == None:
                    good = False
                elif ans[cell.answer] != 0:
                    good = False
    return good

def newString():
    line = 1
    inArray = ["'"]
    for x in range(9):
        inArray.append(raw_input('Nine characters of line ' + str(x+1) + ': '))
    inArray.append("'")
    outStr = ''
    for part in inArray:
        outStr = outStr + part
    print 'inString = ' + outStr

def searchTheRestR(hint, cellSet, segSet):

    def search(hint, searchSet, protectSet):
        searchSetType= searchSet[0].__class__.__name__
        protectSetType = protectSet[0].__class__.__name__
        hintCount = 0
        for seg in searchSet:
            for cell in seg.cells:
                if cell.hints[hint] and cell.getSeg(protectSetType) in protectSet:
                    hintCount += 1
                elif cell.hints[hint] and not cell.getSeg(protectSetType) in protectSet:
                    break
                elif not cell.hints[hint] and not cell.getSeg(protectSetType) in protectSet:
                    pass
                elif not cell.hints[hint] and cell.getSeg(protectSetType) in protectSet:
                    break
            if hintCount == 2:
                return(seg)
        return False

    # Determine if we are working on rows or columns
    searchType = segSet[0].__class__.__name__
    if searchType == 'Row':
        protectType = 'Col'
    elif searchType == 'Col':
        protectType = 'Row'
    else:
        raise ValueError('Passed SearchTheRestR bad segment type')

    # set up protectSet to be opposite of what we are searching through
    protectSet = []
    for cell in cellSet:
        protectSet.append(cell.getSeg(protectType))

    foundSeg = search(hint, segSet, protectSet)
    return foundSeg

def searchSetR(segSet, foundSets=[]):
    if len(segSet) < 2:
        return foundSets
    for hint in range(9):
        hintCnt = 0
        cellSet = []
        for cell in segSet[0].cells:
            if cell.hints[hint] != None:
                cellSet.append(cell)
        if len(cellSet) == 2:
            found = searchTheRestR(hint, cellSet, segSet[1:])
            if found:
                foundSets.append((hint, cellSet, found))
                asdf = 1
    return searchSetR(segSet[1:], foundSets)

#def clearSets(foundSets, game):
#    change = False
#    for foundSet in foundSets:
#        if foundSet[1][0].row == foundSet[1][1].row:
#            #rows match, was searching by row
#            #print 'Found xwing set', foundSet
#            ptSeg1 = foundSet[1][0].row
#            ptSeg2 = foundSet[2]
#            seg1 = foundSet[1][0].col
#            seg2 = foundSet[1][1].col
#            index = 'Cols'
#            hint = foundSet[0]
#            change = cleanSeg(hint, (seg1, seg2), (ptSeg1, ptSeg2), index, game) or change
#        elif foundSet[1][0].col == foundSet[1][1].col:
#            # columns match, was searching by col
#            ptSeg1 = foundSet[1][0].col
#            ptSeg2 = foundSet[2]
#            seg1 = foundSet[1][0].row
#            seg2 = foundSet[1][1].row
#            index = 'Rows'
#            hint = foundSet[0]
#            change = cleanSeg(hint, (seg1, seg2),(ptSeg1, ptSeg2), index, game) or change
#        else:
#            raise ValueError ('Line 580')
#    return change

#def cleanSeg(hint, segments, protect, searchSegs):
#    change = False
#    for seg in segments:
#        for x in range(9):
#            cell = searchSegs[seg].cells[x]
#            if cell.hints[hint] != None and x not in protect:
#                cell.hints[hint] = None
#                change = True
#                print 'Clearing hint:',hint,'in cell', cell, 'Segs:',searchSegs, segments, 'Protect', protect
#    return change

def notList(set):
    """
    Returns ones complement or boolean complement of input set
    @param set: input set
    @return set: return complemented set
    """
    returnSet = []
    for bit in set:
        returnSet.append(not bit)
    return returnSet

def openWeb(inString):
    import webbrowser
    new = 2 # open in a new tab, if possible
    ''' http://www.scanraid.com/sudoku.htm?bd=800207000500400020010000003080000460000901000025000010400000090060003002000509008 '''
    beginning = 'http://www.scanraid.com/sudoku.htm?bd='
    urlString = ''
    for ans in inString:
        if ans == ' ': ans = '0'
        urlString = urlString + ans
    
    # open a public URL, in this case, the webbrowser docs
    url = beginning + urlString
    webbrowser.open(url,new=new)



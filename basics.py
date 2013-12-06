
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

def twoHintSegs(segs, hint):
    '''
    @param hint: Search segs (row, col, or sqr) for pairs of cells with this hint value or range.  Looking for
      sets where those two cells are the only two cells in that seg with that hint set
    @return: list of cell pairs
    '''
    returnSet = []
    if hint:
        hnt_range = range(hint,hint+1)
    else:
        hnt_range = range(9)
    for hint in hnt_range:
        hintCellSet = []
        for segment in segs:
            hintCnt = 0
            cellSet = []
            for cell in segment.cells:
                if cell.hints[hint]:
                    hintCnt += 1
                    cellSet.append(cell)
            if hintCnt == 2:
                hintCellSet.append(cellSet)
        returnSet.append((hint,hintCellSet))
    return returnSet

def is_xwing_quad(pair1, pair2):
    """
    Take two pair of cells, compare columns and rows, return true if these four make an xWing
      quad.  Routine independent of search direction.  Does not check hints, assumes this
      has already been done, just looking at rows and columns
    @param pair1: first pair of cells (in a common row or column)
    @param pair2: second pair of cells (in a common row or column)
    @return: True or false - is this an xWing quad
    """
    pair2Rows = [pair2[0].row,pair2[1].row]
    pair2Cols = [pair2[0].col,pair2[1].col]
    if pair1[0].row in pair2Rows and pair1[1].row in pair2Rows:
        return True
    elif pair1[0].col in pair2Cols and pair1[1].col in pair2Cols:
        return True
    return False

def findCorners(pairs, cellSet):
    """
    Find four corners of an xWing and return the four cells
    @param pairs: [(hint, [cell1, cell2], [cell3, cell4]) ... ]
    @return: cellSet - list of four-cell tuples in xWing
    """
    if len(pairs) < 2:
        return cellSet
    first = pairs[0]

    for second in pairs[1:]:
        if is_xwing_quad(first,second):
            cellSet.append((first,second))
    return findCorners(pairs[1:], cellSet)

def clearCorners(hint, corners):
    """
    corners input in the form [[cell1, cell2], [cell3, cell4]]
    @param corners:
    @return:
    """
    def find_four_segs(cells):
        """
        Take four cells of an x-wing set and return the two rows and two columns (segments
        associated with that square
        @param cells: four cells to process in a list
        @return: four segments in a list
        """
        segs = []
        for cell in cells:
            if cell.row not in segs:
                segs.append(cell.row)
            if cell.col not in segs:
                segs.append(cell.col)
        if len(segs) != 4:
            raise ValueError('Too many segs found in cell set, not x-wings square')
        return(segs)
    def clear_segs(hint, segs, protect):
        """
        Clear the hint 'hint' from each row and column in segs, but protect the four cells in 'protect'
        @param hint: hint to be cleared
        @param segs: four segments that need to be checked
        @param protect: four cells where hint should be protected
        @return: True or False, True if a change was made, False otherwise
        """
        change = False
        for seg in segs:
            change = seg.clearTheseHints(hint, protect, notHint=False, notCells=True) or change
        return change
    change = False
    for segSet in corners:
        cells = segSet[0] + segSet[1]
        fourSegs = find_four_segs(cells)
        print 'SegSet', segSet, 'Corners', corners
        print 'Checking xWing set', hint, cells
        change = clear_segs([hint], fourSegs, cells) or change
    return change

def findPairs(segs, pairSets=[]):
    for hint in range(9):
        for seg in segs:
            pair = [hint]
            cellPair = findPairs(seg, hint)
            if cellPair:
                pair.append(cellPair)
                pairSets.append(pair)
    return pairSets

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
    beginning = 'http://www.scanraid.com/sudoku.htm?bd='
    urlString = ''
    for ans in inString:
        if ans == ' ': ans = '0'
        urlString = urlString + ans
    
    # open a public URL, in this case, the webbrowser docs
    url = beginning + urlString
    webbrowser.open(url,new=new)



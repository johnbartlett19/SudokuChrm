#/bin/python

def input_puzzle():
    """
    Simplifies typing in of puzzle on console.  Call this function, then type in inString values
    one line at a time. Can use zero or space for cells with no answer value.  Prints inString value
    on console when complete.
    """
    inArray = ["'"]
    for x in range(9):
        inArray.append(raw_input('Nine characters of line ' + str(x+1) + ': '))
    inArray.append("'")
    outStr = ''
    for part in inArray:
        outStr = outStr + part
    print 'inString = ' + outStr

def hint_count_sets(segs, hint, count):
    '''
    @param hint: Search segs (row, col, or sqr) for sets of cells with this hint value or range.  Looking for
      sets where those (count) cells are the only (count) cells in that seg with that hint set
    @return: list of cell sets with hint for that pair (hint, [cell1, cell2])
    '''
    returnSet = []
    if hint != None:
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
            if hintCnt == count:
                hintCellSet.append(cellSet)
        returnSet.append((hint,hintCellSet))
    return returnSet


def notList(set):
    """
    Returns ones complement or boolean complement of input set, or opposite set if numbers
    @param set: input set
    @return set: return complemented set
    """
    returnSet = []
    if len(set) == 9: #assume booleans
        for bit in set:
            returnSet.append(not bit)
        return returnSet
    else:
        for x in range(9):
            if x not in set:
                returnSet.append(x)
        return returnSet

def open_web(inString):
    import webbrowser
    new = 2 # open in a new tab, if possible
    beginning = 'http://www.sudokuwiki.org/sudoku.htm?bd='
    urlString = ''
    for ans in inString:
        if ans == ' ': ans = '0'
        urlString = urlString + ans
    url = beginning + urlString
    webbrowser.open(url,new=new)

def all_combo(theSet, count, function, preSet=[], change=False):
    if len(theSet)+len(preSet) < count:
        return change
    preSet = preSet[:] + [theSet[0]]
    mySet = theSet[1:]
    if len(preSet) == count:
        change = function(preSet) or change
        #print change
        theSet.pop(0)
        return all_combo(mySet, count, function, preSet[:-1],change)
    if len(preSet) < count:
        change = all_combo(mySet, count, function, preSet, change) or change
    return all_combo(theSet[1:], count, function, preSet[:-1], change)

def find_twos(cellSet):
    """
    Search through cell set for cells with exactly two hints set
    @param cellSet: simple set of cells
    @return: simple set of cells that have exactly two hints set
    """
    returnSet = []
    for cell in cellSet:
        if cell.countHints() == 2:
            returnSet.append(cell)
    return returnSet

def find_visible_cells(keyCell):
    """
    Find all cells visible to the given cell (same row, col or square) and return a set
      of cells not including given cell, and no duplicates
    @param keyCell: cell from which we are getting visibility
    @return: list of visible cells in a set [cell1, cell2, cell3 ...]
    """
    cellSet = keyCell.row.cells + keyCell.col.cells + keyCell.sqr.cells
    returnSet = []
    for cell in cellSet:
        if cell != keyCell and cell not in returnSet:
            returnSet.append(cell)
    return returnSet

def find_common_cells(cellSet1, cellSet2):
    """
    Given two lists of cells, return the cells that are common to both sets
    @param cellSet1:
    @param cellSet2:
    @return: list of common cells [cell1, cell2, cell3, ...]
    """
    returnSet = []
    for cell in cellSet1:
        if cell in cellSet2:
            returnSet.append(cell)
    return returnSet


def find_ywing_set(cell, cellSet):
    '''
    we assume here that cellSet is visible, and only has two hints true
    search cellSet to see if there is a y-wing set within this cell set
    @param cell: starting cell
    @param cellSet: simple cell set with only two hints set in each cell
    '''
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
    # look in cellSet, find pairs of cells with a common hint that is not one of the
    #   true hints in the original cell
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

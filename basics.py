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
    webbrowser.open(url, new=new)

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
    @return: list of tuples (cell-pair, common-hint)
    '''
    def find_pairs(cell_set, match_hints, return_set=[]):
        '''
        @param: cell-set: list of cells with only two hints set
        @param: match_hints: each cell will match one of these hints, we want a pair where the other hints match
            each other but not the one common with this pair
        @return: List of pairs of cells with common hint in form [([cell1, cell2], hint),(), {}]
        '''
        if len(cell_set) <= 1:
            return return_set
        one = cell_set[0]
        one_hints = one.true_hints()
        for two in cell_set[1:]:
            two_hints = two.true_hints()
            for hint in one_hints:
                for hint2 in two_hints:
                    if hint == hint2 and hint not in match_hints:
                        return_set.append(((one, two), hint))
        return find_pairs(cell_set[1:], match_hints, return_set)
    cell_hints = cell.true_hints()  # get true hints in starter cell
    return find_pairs(cellSet, cell_hints)

def dedupe_pairs(pairs):
    """
    Take a list of cell pairs and eliminate duplications
    @param pairs: set of cell pairs in the form [[cell1, cell2],[cell3, cell4],...]
    @return: set of deduped cell pairs in the same format
    """
    returnSet = []
    for pair in pairs:
        flip = [pair[1],pair[0]]
        if pair not in returnSet and flip not in returnSet:
            returnSet.append(pair)
    return returnSet

def dedupe_pairs_with_hint(pairs):
    """
    Take a list of cell pairs and eliminate duplications
    @param pairs: set of cell pairs in the form [(hint,[[cell1, cell2],[cell3, cell4],...]),...]
    @return: set of deduped cell pairs in the same format
    """
    returnSet = []
    for hint, cellSet in pairs:
        returnCellSet = []
        for pair in cellSet:
            pair_sorted = sorted(pair)
            if pair_sorted not in returnCellSet:
                returnCellSet.append(pair_sorted)
        returnSet.append((hint,returnCellSet))
    return returnSet

def not_cell(cell, pair):
    if cell == pair[0]:
        return pair[1]
    elif cell == pair[1]:
        return pair[0]
    else:
        raise ValueError('Cell not in pair')
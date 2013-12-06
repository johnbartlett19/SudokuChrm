#/bin/python
import copy
from basics import *
from simpleColoredChain import *

def countHints(cellArray):
    cntArray = [0 for x in range(9)]
    for cell in cellArray:
        for hint in range(9):
            if cell.hints[hint] != None:
                cntArray[hint] += 1
    return cntArray

class Cell(object):
    def __init__(self, row, col, square, game):
        self.answer = None
        self.hints = [True for x in range(9)]
        self.row = row
        self.col = col
        self.sqr = square
        self.game = game

    def __repr__(self):
        return 'Cell-' + str(self.row) + '-' + str(self.col) #+ '-' + str(self.sqr)

    def getSeg(self,segType):
        if segType == 'Row':
            return self.row
        elif segType == 'Col':
            return self.col
        elif segType == 'Sqr':
            return self.sqr
        else:
            raise ValueError('Passed cell.getSeg() a bad segType value')
        return

    def setAnswer(self, ans):
        ''' set the answer for this cell'''
        self.answer = ans
        self.hints = [None for x in range(9)]
    def clearHints(self, hints):
        ''' clear the numbered hints in hints from this cell, return True if
            changes were made, else return False '''
        change = False
        for hint in hints:
            if self.hints[hint]:
                self.hints[hint] = None
                change = True
        if self.countHints() == 0 and self.answer == None:
            raise ValueError('Just cleared last hint in a cell', self)
        return change
    def countHints(self):
        count = 0
        for x in range(9):
            if self.hints[x]:
                count += 1
        return count

class Group(object):
    def __init__(self, num, game):
        self.cells = []
        #self.position = []
        self.num = num
        self.game = game

    def addCell(self, cell):
        ''' add a cell to this segment (row, col, square) '''
        self.cells.append(cell)

    def clearHints(self):
        ''' find current answers in this segment, clear all hints for those answers
            and return True if any changes were made, else return False '''
        answers = []
        for cell in self.cells:
            if cell.answer != None:
                answers.append(cell.answer)
        change = False
        for cell in self.cells:
            if cell.clearHints(answers):
                    change = True
        return change

    def twoHintCellPair(self, hint):
        pair = []
        for cell in self.cells:
            if cell.hints[hint]:
                pair.append(cell)
        if len(pair) == 2:
            return pair
        return False

    def singleRCS(self):
        hintCount = [0 for x in range(0,9)]
        for cell in self.cells:
            for x in range(0,9):
                if cell.hints[x]:
                    hintCount[x] += 1
        for x in range(0,9):
            if hintCount[x]==1:
                for cell in self.cells:
                    if cell.hints[x]:
                        cell.setAnswer(x)
                        print 'Found single RCS', cell, 'value', cell.answer
                        return True
        return False

    def solveNakedPair(self):            
        def findNakedPair(cellArray):
            cell = cellArray[0]
            if len(cellArray) == 1:
                return False
            elif cell.countHints() == 2:
                for compCell in cellArray[1:]:
                    if cell.hints == compCell.hints:
                        return (cell, compCell)
            return findNakedPair(cellArray[1:])

        change = False
        found = findNakedPair(self.cells)
        if found:
            print 'Found naked pair', found
            hintSet = []
            for x in range(9):
                if found[0].hints[x]:
                    hintSet.append(x)
            for cell in self.cells:
                if cell not in found:
                    for hint in hintSet:
                        if cell.hints[hint]:
                            cell.clearHints([hint])
                            change = True
        return change

    def solveNakedSets(self, count):
        '''
        Naked sets are sets of 2, 3 or 4 cells with 2, 3 or 4 hints total.  If a naked set exists, the hints in
         the naked set can be removed from any cells not in the naked set
        @param count: number of cells & hints for this search
        @return: change (True/False) if a change was made
        '''
        def noEmptySets(cellArray):
            """
            Remove any cells from this set that have no hints
            @param cellArray: list of cells to scrub
            @return: scrubbed cell array
            """
            newSet = []
            for cell in cellArray:
                if cell.countHints() != 0:
                    newSet.append(cell)
            return newSet
        def matchHints(baseHints, newHints, orSet):
            """
            Create a set of True/False bits for a set of hints so that we can see all the hints set
             in the naked set.  orSet is passed in so that this routine can be run multiple times
            @param baseHints: starting set of hints
            @param newHints: set to be compared against base
            @param orSet: OR of true bits from previous compares
            @return: (count, orSet).  Count is the number of bits set in orSet
            """
            for x in range(9):
                if baseHints[x] or newHints[x]:
                    orSet[x] = True
            count = 0
            for x in range(9):
                if orSet[x]:
                    count += 1
            return (count,orSet)
        def findNakedSet(cellArray, count):
            """
            Recursive search of cellArray cells to find a set of length count
            @param cellArray: cell set to search
            @param count: size of set we are searching for
            @return: set of cells that form the naked set, or False if not found
            """
            if len(cellArray) < count:
                return False
            cellSet = []
            cell = cellArray[0]
            if cell.countHints() <= count:
                cellSet.append(cell)
                baseSet = [None for x in range(9)]
                for compCell in cellArray[1:]:
                    orSet = copy.deepcopy(baseSet)
                    cnt, orSet = matchHints(cell.hints, compCell.hints, orSet)
                    if cnt <= count:
                        cellSet.append(compCell)
                        baseSet = copy.deepcopy(orSet)
                if len(cellSet) == count:
                    return cellSet
            return findNakedSet(cellArray[1:], count)

        change = False
        found = findNakedSet(noEmptySets(self.cells), count)
        if found:
            hintSet = []
            
            for x in range(9):
                for cell in found:
                    if cell.hints[x]:
                        if cell.hints[x] not in hintSet:
                            hintSet.append(x)
            for cell in self.cells:
                if cell not in found:
                    for hint in hintSet:
                        if cell.hints[hint]:
                            cell.clearHints([hint])
                            change = True
                            print 'Found Naked Set', found, 'Cleared bits', hint
        return change

    def solveHiddenSets(self,count):
        def trueCnt(set):
            trueCnt = 0
            for x in range(9):
                if set[x]: trueCnt += 1
            return trueCnt
                        
        def cleanSet(mySet):
            cleanSet = []
            for x in range(9):
                if trueCnt(mySet[x]) != 0:
                    cleanSet.append(mySet[x])
            return cleanSet

        def orSet(orSet, orSum):
            mySum = copy.deepcopy(orSum)
            bitCount = 0
            for x in range(9):
                if orSet[x]:
                    mySum[x] = mySum[x] | orSet[x]
                if mySum[x] == 1:
                    bitCount += 1
            return (bitCount, mySum)
                    
        def chkRest(ckSet, count, orSum):
            for grp in ckSet:
                cnt, sumx = orSet(grp, orSum)
                if cnt == count:
                    return grp
            return False

        def checkFirstNofSet(set, count):
            if len(set) < count:
                return False
            hintSet = []
            set1 = copy.deepcopy(set)
            orSum = [0 for x in range(9)]
            for x in range(count-1):
                cnt, orSum = orSet(set1[x], orSum)
                hintSet.append(set1[x][9])
            found = chkRest(set1[(count-1):], count, orSum)
            if found:
                hintSet.append(found[9])
                if(self.clearHintsHidden(orSum, hintSet)):
                    return True
            set.pop(1)
            return checkFirstNofSet(set,count)

        def checkSet(set,count):
            if len(set) < count:
                return False
            workingSet = copy.deepcopy(set)
            if checkFirstNofSet(workingSet, count):
                print 'Found set and cleared bits'
                return True
            else:
                workingSet = copy.deepcopy(set)
                workingSet.pop(0)
                return checkSet(workingSet,count)

        change = False
        # create array of hint locations
        hintArray = [[self.cells[cell].hints[hint] for cell in range(9)] for hint in range(9)]

        for cell in range(9):
            hintArray[cell].append(cell)
        return (checkSet(cleanSet(hintArray),count))

    def clearHintsHidden(self,orSum, hintSet):
        def comp(hintSet):
            notSet = []
            for hint in range(9):
                if hint not in hintSet:
                    notSet.append(hint)        
            return notSet
        change = False
        count = 0
        for x in range(9):
            count += orSum[x]
        for cell in range(9):  # Cells
            if orSum[cell] == 1:  # if orSum has it marked
                change = self.cells[cell].clearHints(comp(hintSet)) or change
            else:
                change = self.cells[cell].clearHints(hintSet) or change
        return change

    def findPointingPair(self):
        cntArray = countHints(self.cells)
        superSet = []
        for cnt in range(9):
            if cntArray[cnt] > 1 and cntArray[cnt] < 4:
                # find cells with these bits
                cellSet = []
                for cell in self.cells:
                    if cell.hints[cnt] != None:
                        cellSet.append(cell)   # find cells with 2 or three hints only
                row = 'a'
                col = 'a'
                sqr = 'a'
                for cell in cellSet:
                    if row == 'a':
                        row = cell.row
                    else:
                        if row != cell.row:
                            row = None
                    if col == 'a':
                        col = cell.col
                    else:
                        if col != cell.col:
                            col = None
                    if sqr == 'a':
                        sqr = cell.sqr
                    else:
                        if sqr != cell.sqr:
                            sqr = None
                if (row != None or col != None) and sqr != None:
                    superSet.append((row,col,sqr,cellSet,cnt))
        return superSet

    def cleanSeg(self, hint, protect):
        """
        Remove the hint 'hint' from all cells in this segment except in those cells that belong
         to the segments in the 'protect' string
        @param hint: integer between 0 and 8, a hint value
        @param protect: list of segments (rows, cols, squares) to be protected
        @return: True if cell hints were changed, False otherwise
        """
        def cellInProtect(cell, protect):
            for seg in protect:
                if cell in seg.cells:
                    return True
            return False
        change = False
        for cell in self.cells:
            if cell.hints[hint] and not cellInProtect(cell,protect):
                change = cell.clearHints([hint]) or change
                print 'Clearing hint:', hint, 'in cell', cell, 'Seg:', self, 'Protect', protect
        return change

    def clearTheseHints(self, hints, cells, notHint=False, notCells=False):
        """
        More generic hint clearing
        @param hints: list of hints to be cleared, nine long, None, False or True
        @param cells: list of cells on which to operate, individual cells
        @param notHint: if True, clear hints not in hint list instead of hints
        @param notCells: if True, clear cells not on cell list instead of cells
        @return True if hints were cleared, otherwise False
        """
        if len(hints) == 9:
            raise ValueError('Received list of Booleans not hint list', hints)
        if notHint:  # invert hint array if notHint is true
            hintList = notList(hints)
        else:
            hintList = hints
        cellList = []
        if notCells: # get cells not on cell list if notCells is true
            for cell in self.cells:
                if cell not in cells:
                    cellList.append(cell)
        else:
            cellList = cells
        change = False
        for cell in cellList: #do the clearing of hints
            if cell in cellList:
                change = cell.clearHints(hintList) or change
        return change

class Row(Group):
    def __init__(self, num, game):
        Group.__init__(self, num, game)
        pass
    def __repr__(self):
        return 'R' + str(self.num)
    def __name__(self):
        return 'Row'

class Col(Group):
    def __init__(self, num, game):
        Group.__init__(self, num, game)
        pass
    def __repr__(self):
        return 'C' + str(self.num)
    def __name__(self):
        return 'Col'
    
class Square(Group):
    def __init__(self, num, game):
        Group.__init__(self, num, game)
        pass
    def __repr__(self):
        return 'S' + str(self.num)
    def __name__(self):
        return 'Sqr'

class Chain(object):
    def __init__(self, hint):
        self.hint = hint
        self.nodes = []
        self.colored = False
    def __repr__(self):
        return 'Chain H', self.hint
    def color(self):
        # color this chain
        def colorChain(node, last='Blue'):
            if last == 'Blue':
                node.color = 'Red'
            elif last == 'Red':
                node.color = 'Blue'
            for nodeLink in node.links:  # follow the links
                if nodeLink.color == None:
                    colorChain(nodeLink, node.color)
        if len(self.nodes) < 2:
            raise ValueError('Coloring a chain less than two nodes long')
        if self.colored:
            raise ValueError('Coloring a colored chain')
        colorChain(self.nodes[0])

class Game(object):
    # rewrite this init from scratch.  Set up segs to know which game they belong to.
    # set up cells to know which row, col and square they belong to.  Have to initiate
    # from game down to lower levels.
    def __init__(self):
        self.cells = []
        self.rows = [Row(x,self) for x in range(9)]
        self.cols = [Col(x,self) for x in range(9)]
        self.sqrs = [Square(x,self) for x in range(9)]
        self.segs = [self.rows,self.cols,self.sqrs]
        for row in range(0,9):
            for col in range(0,9):
                square = int((row)/3)*3 + int((col)/3)
                cell = Cell(self.rows[row],self.cols[col],self.sqrs[square], self)
                self.cells.append(cell)
                self.rows[row].addCell(cell)
                self.cols[col].addCell(cell)
                self.sqrs[square].addCell(cell)

    def getSegs(self,segType):
        if segType == 'Row':
            return self.rows
        elif segType == 'Col':
            return self.cols
        elif segType == 'Sqr':
            return self.sqrs
        else:
            raise ValueError('Passed cell.getSeg() a bad segType value')
        return

    def printHints(self, mode):
        printArray = [[[ ' ' for x in range(0,9)] for x in range(0,9)] for x in range(0,9)]
        for cell in self.cells:
            for x in range(0,9):
                if cell.answer == None:
                    if cell.hints[x]:
                        printArray[cell.row.num][cell.col.num][x] = x + mode
                    else:
                        printArray[cell.row.num][cell.col.num][x] = ' '
                else:
                    printArray[cell.row.num][cell.col.num][x] = cell.answer + mode
        print '=' * 73
        for row in range(0,9):
            for hintRow in range(0,3):
                print 'H',
                for col in range(0,9):
                    for hintCol in range(0,3):
                        hintNum = (hintRow * 3 + hintCol)
                        print printArray[row][col][hintNum],
                    if (col+1)%3 == 0:
                        print 'H',
                    else:
                        print '|',
                print
            if (row+1)%3 == 0:
                print '=' * 73
            else:
                print '-' * 73

    def __repr__(self):
        return 'Game'

    def clearHints(self):
        print 'Clearing hints by answers', self
        for row in self.rows:
            row.clearHints()
        for col in self.cols:
            col.clearHints()
        for sqr in self.sqrs:
            sqr.clearHints()

    def setGameStart(self, inString):
        for cell in self.cells:
            cellNum = 9 * (cell.row.num) + (cell.col.num)
            if inString[cellNum] != '0' and inString[cellNum] != ' ':
                cell.setAnswer(int(inString[cellNum])-1)

    def check(self):
        good = True
        for row in self.rows:
            ans = [None for x in range(9)]
            for x in range(9):
                cell = row.cells[x]
                if cell.answer == None:
                    good = False
                elif ans[cell.answer] != None:
                    good = False
                else:
                    ans[cell.answer] = True
        return good

    def printAnswers(self, mode):
        printArray = [[ 0 for x in range(0,9)] for x in range(0,9)]
        for cell in self.cells:
            if cell.answer == None:
                ans = ' '
            else:
                ans = cell.answer + mode
            printArray[cell.row.num][cell.col.num] = ans

        for row in range(0,9):
            if row % 3 == 0:
                print '-' * 25
            for col in range(0,9):
                if col % 3 == 0:
                    print '|',
                print printArray[row][col],
            print '|'
        print '-' * 25

    def solveSingle(self):
        print 'checking for singles'
        change = False
        for cell in self.cells:
            hintCount = 0
            for hint in range(9):
                if cell.hints[hint]:
                    hintCount += 1
                    hintAns = hint
            if hintCount == 1:
                cell.answer = hintAns
                print 'Found Single Answer',cell, 'value', cell.answer
                change = True
        return change

    def solveSingleRCS(self):
        print 'checking for single RCS'
        for group in self.segs:
            for seg in group:
                if seg.singleRCS():
                    return True
        return False

    def solveNakedSets(self):
        for setSize in range(2,5):
            print 'Checking for naked sets size', setSize
            for group in self.segs:
                for seg in group:
                    if seg.solveNakedSets(setSize):
                        return True
        return False

    def solveHiddenSets(self):
        for setSize in range(2,5):
            print 'Checking for hidden sets size ', setSize
            for group in self.segs:
                for seg in group:
                    if seg.solveHiddenSets(setSize):
                        return True
        return False

    def solvePointingSets(self):
        print 'Checking for pointing sets'
        change = False
        for square in self.sqrs:
            pairSets = square.findPointingPair()
            for row,col,sqr,cells,hint in pairSets:
                if row != None:
                    #change = self.rows[row].clearPtPairHints(cells, hint) or change
                    change = row.clearTheseHints([hint],cells,notCells=True) or change
                elif col != None:
                    #change = col.clearPtPairHints(cells, hint) or change
                    change = col.clearTheseHints([hint],cells,notCells=True) or change
        return change

    def boxLineReduction(self):
        print 'Checking box line reductions'
        change = False
        segs = self.rows + self.cols
        change = False
        for seg in segs:
            pairSets = seg.findPointingPair()
            for row,col,sqr, cells,hint in pairSets:
                #change = self.sqrs[sqr].clearPtPairHints(cells, hint) or change
                change = sqr.clearTheseHints([hint],cells,notCells=True) or change
        return change

    def solveXwings(self):
        """
        Find x-wings pairs, clear any hints eliminated by x-wing pair
        @return: True if any hints were deleted, otherwise false
        """
        self.printHints(False)
        change = False
        segSets = [self.rows, self.cols] # will search by rows then by columns
        for segs in segSets:
            print 'Checking xWings', segs
            # get a list of all cells in this seg set that have only two hints
            pairs = twoHintSegs(segs, None) # None means all hints
            # find all x-wing sets (two rows with matching hints per column and vice versa
            # return list of the four cell combinations
            for (hint, set_of_one_hint) in pairs:
                cellSet = []
                corners = findCorners(set_of_one_hint, cellSet)
            # now set up to do the clearing.  We can clear for rows and columns, no need to sort it out.
                change = clearCorners(hint, corners) or change
        return change

    def clearSets(self, foundSets):
        change = False
        print 'xWings foundSets', foundSets
        for foundSet in foundSets:
            if foundSet[1][0].row == foundSet[1][1].row:
                #rows match, was searching by row
                ptSeg1 = foundSet[1][0].row
                ptSeg2 = foundSet[2]
                seg1 = foundSet[1][0].col
                seg2 = foundSet[1][1].col
                #searchSegs = self.cols
                hint = foundSet[0]
                #change = self.cleanSeg(hint, (seg1, seg2), (ptSeg1, ptSeg2), searchSegs) or change
            elif foundSet[1][0].col == foundSet[1][1].col:
                # columns match, was searching by col
                ptSeg1 = foundSet[1][0].col
                ptSeg2 = foundSet[2]
                seg1 = foundSet[1][0].row
                seg2 = foundSet[1][1].row
                #searchSegs = self.rows
                hint = foundSet[0]
            else:
                raise ValueError ('')
            #self.printHints(False)
            raise ValueError(hint, ptSeg1, ptSeg2)
            #change = seg1.clearTheseHints([hint], cells, notHint=False, notCells=False)
            # pass forward the protected segments, not integers
            #cleanSeg(self, hint, protect):
            change = seg1.cleanSeg(hint, (ptSeg1, ptSeg2)) or change
            change = seg2.cleanSeg(hint, (ptSeg1, ptSeg2)) or change

            #change = cleanSeg(hint, (seg1, seg2),(ptSeg1, ptSeg2), searchSegs) or change
        return change

    def findXwingQuads(segs, segType, cntrType, foundPairs=[]):
        if len(segs) < 2:
            return foundPairs

    def findCommonSeg(self,tuple):
        """
        @param tuple: contains two nodes of a chain
        @return tuples (1 or 2) as a list, first element is the segment index these two cells have in common,
          the second is a list of the two positions in that segment where these cells reside (to be protected
          in a clean for example) (e.g. [(row[3],([2,4]),(sqr[3],(3,5))]
        """
        def findPosition(tuple, thisSeg):
            ''' find position of two cells in tuple in the row thisRow
            @param tuple: two cells
            @param thisSeg: segment within which the two cells should be located
            @return:
            '''
            position = []
            for x in range(9):
                if thisSeg.cells[x] in tuple:
                    position.append(x)
            return position
        returnSet = []
        cellPair = (tuple[0].cell,tuple[1].cell)
        position = findPosition(cellPair, self.rows[cellPair[0].row])
        if len(position) == 2:
            returnSet.append((self.rows[cellPair[0].row],position))
        position = findPosition(cellPair, self.cols[cellPair[0].col])
        if len(position) == 2:
            returnSet.append((self.cols[cellPair[0].col],position))
        position = findPosition(cellPair, self.sqrs[cellPair[0].sqr])
        if len(position) == 2:
            returnSet.append((self.sqrs[cellPair[0].sqr],position))
        return returnSet

    def simpleColoring(self):
        def dedupe_pairs(pairs):
            """
            Take a list of cell pairs and eliminate duplications
            @param pairs: set of cell pairs in the form [[cell1, cell2],[cell3, cell4],...]
            @return: set of deduped cell pairs in the same format
            """
            returnSet = []
            for pair in pairs:
                flip = (pair[0],[pair[1][1], pair[1][0]])
                if pair not in returnSet and flip not in returnSet:
                    returnSet.append(pair)
            return returnSet
        def get_cell_pairs():
            """
            Find all cell pairs in the game where the segment (row, col, sqr) has only two cells
            for any given hint
            @return: cell pairs in the form [[cell1, cell2],[cell3, cell4],...]
            """
            change = False
            segs = self.rows + self.cols + self.sqrs
            coloredChains = []
            for hint in range(3,4):  # **** Only working on known problem, need to open this up to all hints
                # find all segments where a hint shows up only twice
                pairs = twoHintSegs(self.rows, hint) + twoHintSegs(self.cols, hint) + twoHintSegs(self.sqrs, hint)
                #pairs = twoHintSegs(segs, hint) # None means all hints
                # remove duplications from squares
                pairs = dedupe_pairs(pairs)
                print pairs
                # Pull out the cell-pairs only, dropping the initial hint
                pairs_no_hint = []
                for pair in pairs:
                    pairs_no_hint.append(pair[1])
            return pairs_no_hint

        def create_chains(pairs):
            # create chains
            """
            Take a set of cell pairs, create nodes of a chain and color the chains.  Return a list
              of colored chains
            @param pairs: list of cell pairs in the form [[cell1, cell2],[cell3, cell4],...]
            @return: list of colored chains in the form[[node1, node2, node3, node4],[node ...], ...]
            """
            chains = createChains(pairs)
            # color the chains
            for chain in chains:
                chain.color()
                printChain(chain)
                print()
            return chains

        def rule_two(chain):
            """
            Rule 2: This Rules says that if any seg has the same color twice
              ALL those candidates which share that colour must be OFF.
            @param hint: active hint for this chain
            @param chain:
            @return: change = True if hints were cleared, otherwise false:
            """
            change = False
            pass
            return change

        def rule_four(chain):
            """
            Rule 4: If a segment has both a red and green node, the hint can be deleted in all other
              cells of the segment
            @param hint:
            @param chain:
            @return: change = True if hints were cleared, otherwise false
            """
            change = False
            #if len(dd) > 0:
            #    print 'DD', dd
            #    result = self.findCommonSeg(dd)
            #    #### result should now be a set of common row or col or squares (maybe two out of three)
            #    print result
            #    cleanSeg(hint, segments, protect, index, game)
            #    raise ValueError('Found Simple Colored Chain Rule 4, not implemented', dd)
            #print 'Rule Four', dd, hint
            return change

        def rule_five(chain):
            """
            Rule 5:  If a cell is visible by both a red and green cell of a chain, then the hint can be
              eliminated in that cell
            @return: change = True if hints were cleared, otherwise false
            """
            change = False
            return change

        change = False
        pairs = get_cell_pairs()
        chains = create_chains(pairs)
        for chain in chains:
            change = rule_two(chain) or change
            change = rule_four(chain) or change
            change = rule_five(chain) or change
        # need to put the hint into the chain, go back and figure out where that belongs
        return change



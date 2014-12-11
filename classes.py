#/bin/python
import copy
from basics import *
from simpleColoredChain import *
#from yWings import *


class Cell(object):
    '''
    Represents a cell in the Sudoku puzzle.  Initially has 9 true hints meaning it could be any of 9 answers
    Hints are represented as 0 thru 8 to make them more consistent with Python and allow use of simple ranges
    Printout of the puzzle at the end of the program adds one to each hint to make more consistent with how puzzles
    are typically presented.

    Each cell knows to which row, column and square it belongs, and also to the whole game.  This allows finding of
    visible cells (for instance) by working back to the larger set.
    '''
    def __init__(self, row, col, square, game):
        self.answer = None
        self.hints = [True for x in range(9)]
        self.row = row
        self.col = col
        self.sqr = square
        self.segs = [self.row, self.col, self.sqr]
        self.game = game

    def __repr__(self):
        return 'Cel-' + str(self.row) + '-' + str(self.col) #+ '-' + str(self.sqr)
    def __lt__(self, other):
        return [str(self.row), str(self.col), str(self.sqr)] < [str(other.row), str(other.col), str(other.sqr)]

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
                print 'Cleared hint ' + str(hint + 1) + ' in ' + str(self)
                change = True
        if self.countHints() == 0 and self.answer == None:
            raise ValueError('Just cleared last hint in a cell ', self)
        return change

    def countHints(self):
        '''
        Count how many hints are set true
        @return: integer count of true hints
        '''
        count = 0
        for x in range(9):
            if self.hints[x]:
                count += 1
        return count

    def true_hints(self):
        '''
        @return: array of index of true hints e.g. [2,3]
        '''
        true_hints = []
        for x in range(9):
            if self.hints[x]:
                true_hints.append(x)
        return true_hints

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

    def hints_in_seg(self, hint):
        '''
        Count the number of cells with 'hint' true
        @param hint: hint value to check
        @return: count of cells (integer 0-9) with hint true
        '''
        cellCount = 0
        for cell in self.cells:
            if cell.hints[hint]:
                cellCount += 1
        return cellCount

    def twoHintCellPair(self, hint):
        '''
        Determine if group has only 2 cells with 'hint' value true
        @param hint: hint value to check
        @return: pair of cells if there are only two with hint set, otherwise False
        '''
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

    def cells_with_hint(self, hint):
        '''
        Find all cells in group with hint true, return set, return False if none
        @param hint: value of hint to check
        @return: set of cells or False
        '''
        hint_set = []
        for cell in self.cells:
            if cell.hints[hint]:
                hint_set.append(cell)
        if len(hint_set) > 0:
            return hint_set
        else:
            return False

    def solve_naked_sets(self, count):
        """
        second generation code, using the 'all_combo' function for searching through sets in combinations
        Check this segment (self) for naked pairs, triples, quads
        @param count: size of naked set (in cells) we are searching
        @return: True if hint changes were made, otherwise false
        """
        def remove_empty_cells(cellArray):
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

        def count_hint_types(cellArray):
            count = 0
            hintArray = [None for x in range(9)]
            for x in range(9):
                for cell in cellArray:
                    hintArray[x] = hintArray[x] or cell.hints[x]
                if hintArray[x]:
                    count += 1
            return count, hintArray

        def naked_set(cellArray):
            """
            Check cell array for presence of naked set.  If set is a naked set, clear hints of this set
             in all other cells of the segment, not in this set
            @param cellArray: cell set to search
            @return: True if found a naked set and cleared at least one hint, otherwise False
            """
            change = False
            count, hintArray = count_hint_types(cellArray)
            if count == len(cellArray):
                change = self.clear_these_hints(hintArray,cellArray,notCells=True) or change
            return change

        return all_combo(self.clean_set(),count,naked_set)

    def clean_set(self):
        clean_set = []
        for cell in self.cells:
            if cell.countHints() != 0:
                clean_set.append(cell)
        return clean_set

    def solve_hidden_sets(self,count):

        def hints_less_than(count):
            """
            Search cells of segment, count hints of each type, return a list
             of hints that only appear count or fewer times
            @param count: count limit
            @return: set of hint values e.g. [0,3,4,7] that occur count or fewer times in cell array
            """
            returnSet = []
            for hint in range(9):
                cnt = 0
                for cell in self.cells:
                    if cell.hints[hint]:
                        cnt += 1
                if cnt <= count and cnt > 0:
                    returnSet.append(hint)
            return returnSet

        def solve_hidden(set, hints, fullSet):
            # find 'count' hints that are in this set and not in the rest of the cells of the segment (clean)
            def hint_in_set(hint, set):
                # return true if hint is in at least one cell of set, otherwise False
                for cell in set:
                    if cell.hints[hint]:
                        return True
                return False

            def hint_not_in_rest(hint, set, fullSet):
                # return True if hint is not in any cell of fullSet except those in set
                for cell in fullSet:
                    if cell not in set and cell.hints[hint]:
                        return False
                return True

            change = False
            good_hints = []
            for hint in hints:
                if hint_in_set(hint,set) and hint_not_in_rest(hint, set, self.cells):
                    good_hints.append(hint)
            if len(good_hints)== count:
                change = self.clear_these_hints(hints,set,notHint=True) or change
            return change

        hints = hints_less_than(count)
        full_set = self.clean_set()
        return all_combo(full_set,count,lambda set: solve_hidden(set, hints, full_set))

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

    def countHints(self):
        """
        Counts the number of hints of each type in the cell array of this segment
        @return: array 0-8 with a count of each hint type
        """
        cntArray = [0 for x in range(9)]
        for cell in self.cells:
            for hint in range(9):
                if cell.hints[hint] != None:
                    cntArray[hint] += 1
        return cntArray

    def find_pointing_pair(self):
        """
        If there are two or three cells in a segment that are the only two or three with a given hint, and if those two
        cells are in a common row or column and a common square, return the two cells and the hint value
        @return: an array of [(row, col, sqr, cellSet, cnt),(...)]
        """
        cntArray = self.countHints()
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

    def clear_these_hints(self, hints, cells, notHint=False, notCells=False):
        """
        More generic hint clearing
        @param hints: list of hints to be cleared, nine long, None, False or True, or a list of hint numbers
          e.g. [2,5,7]
        @param cells: list of cells on which to operate, individual cells
        @param notHint: if True, clear hints not in hint list instead of hints
        @param notCells: if True, clear cells not on cell list instead of cells
        @return True if hints were cleared, otherwise False
        """
        if len(hints) == 9:
            boolHints = hints[:]
            hints = []
            for x in range(9):
                if boolHints[x] > 1:
                    raise ValueError('Thought these were boolean, appear to be values')
                elif boolHints[x]:
                    hints.append(x)
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

class ChainNode(object):
    def __init__(self, cell):
        self.cell = cell
        self.color = None
        self.links = []
    def __repr__(self):
        return 'ChNode-' + str(self.cell) + '-' + str(self.color)
    def __len__(self):
        return len(self.links)
    def has_cell(self, cell):
        if cell in [self.node_1, self.node_2]:
            return True
        return False
    def addLink(self, node):
            self.links.append(node)

class Chain(object):
    def __init__(self, hint, node, type='X'):
        def build(chain, node):
            chain.nodes.append(node)
            for link in node.links:
                if link not in chain.nodes:
                    build(chain, link)
        self.hint = hint
        self.nodes = []
        self.name = str(node)
        self.type = type
        build(self, node)

    def __repr__(self):
        return 'Chain-H' + str(self.hint) + '-' + self.type + '-' + self.name

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
        if self.nodes[0].color != None:
            raise ValueError('Coloring a colored chain')
        colorChain(self.nodes[0])

    def rule_two(self):
        """
        Rule 2: This Rules says that if any seg has the same color twice
          ALL those candidates which share that color must be OFF.
        @return: change = True if hints were cleared, otherwise false:
        """
        def find_rule_two(nodes):
            if len(nodes) < 2:
                return False
            lead = nodes[0]
            for node in nodes[1:]:
                if nodeComp(lead,node) and lead.color == node.color:
                    return(lead, node)
                return find_rule_two(nodes[1:])
            return False
        print 'Checking coloring Rule 2'
        change = False
        nodes = find_rule_two(self.nodes)
        if nodes:
            # clear hints in these two nodes, mark change as true, return change
            for node in nodes:
                change = node.cell.clearHints([self.hint]) or change
        return change

    def rule_four(self):
        """
        Rule 4: If a segment has both a red and green node, the hint can be deleted in all other
          cells of the segment
        @param hint:
        @param chain:
        @return: change = True if hints were cleared, otherwise false
        """
        def find_rule_four(nodes):
            if len(nodes) < 2:
                return False
            lead = nodes[0]
            for node in nodes[1:]:
                commonSeg = nodeComp(lead,node)
                if commonSeg and lead.color != node.color:
                    return(lead, node, commonSeg)
                return find_rule_four(nodes[1:])
            return False
        print 'Checking coloring Rule 4'
        change = False
        nodes = find_rule_four(self.nodes)
        if nodes:
            # clear hints in all cells of the segment except the two in the chain
            cells = [nodes[0].cell, nodes[1].cell]
            seg = nodes[2]
            change = seg.clear_these_hints([self.hint], cells, notCells=True) or change
        return change

    def rule_five(self):
        """
        Rule 5:  If a cell is visible by both a red and green cell of a chain, then the hint can be
          eliminated in that cell
        @return: change = True if hints were cleared, otherwise false
        """
        #for each pair of cells in the chain (recursive function again):
        #  find cells with different colors
        #  find cells visible to each cell
        #  find cells common in visibility
        #  clear hint in commonly visible cells
        #  return True if a change was made
        def find_rule_five(nodes, hint, change):
            if len(nodes) < 2:
                return change
            lead = nodes[0]
            for node in nodes[1:]:
                if lead.color != node.color:
                    vis1 = find_visible_cells(lead.cell)
                    vis2 = find_visible_cells(node.cell)
                    visible_to_both = find_common_cells(vis1, vis2)
                    if visible_to_both:
                        for cell in visible_to_both:
                            change = cell.clearHints([self.hint]) or change
            return find_rule_five(nodes[1:], hint, change)
        print 'Checking coloring Rule 5'
        change = False
        return find_rule_five(self.nodes,self.hint,change)

class XChain_Link(object):
    def __init__(self, type, hint, pair):
        if type in ['Strong', 'Weak']:
            self.type = type
        else:
            raise ValueError('Trying to create XChainNode of type ' + type)
        self.node_1, self.node_2 = sorted(pair)
        self.cells = [self.node_1, self.node_2]
        self.hint = hint

    def __repr__(self):
        return 'XChLnk-' + str(self.node_1) + '-' + str(self.node_2)

class XChain(object):
    def __init__(self):
        self.links = []
        self.head = None
        self.tail = None
        self.loop = False
        self.head_cell = None
        self.tail_cell = None
        self.hint = None

    def __repr__(self):
        return 'XChain ' + str(len(self.links))

    def str_links(self):
        nxt_cell = self.head_cell
        for link in self.links:
            print nxt_cell,
            print '~',
            nxt_cell = not_cell(nxt_cell, [link.node_1, link.node_2])
            # if nxt_cell == self.tail_cell:
            #     break
        print nxt_cell
            
    def add_link(self, new_link, end):
        if self.head == None and self.tail == None:
            # first link in this chain
            self.links.append(new_link)
            self.head = new_link
            self.tail = new_link
            self.head_cell = new_link.node_1
            self.tail_cell = new_link.node_2
            self.hint = new_link.hint
        else:
            found = False
            # make sure hint of link matches chain
            if self.hint != new_link.hint:
                raise ValueError('Adding XChainLink to XChain with non-matching hint value')
            new_pair = [new_link.node_1, new_link.node_2]
            if end == 'Tail' and self.tail_cell in new_pair:
                # insert at end
                self.tail = new_link  # make new link new tail
                # new_link.node_linked(cell) # set cell in new tail as linked
                self.links = self.links + [new_link]
                self.tail_cell = not_cell(self.tail_cell, new_pair)
            elif end == 'Head' and self.head_cell in new_pair:
                # insert at head
                self.head = new_link  # set head as new link
                self.links = [new_link] + self.links
                self.head_cell = not_cell(self.head_cell, new_pair)
            else:
                raise ValueError('Trying to add link to chain with no match')
        if self.head_cell == self.tail_cell:
            self.loop = True
            return True
        else:
            if self.loop:
                raise ValueError ("Why wasn't loop caught and corrected?")
        return False

    def remove_link(self, link):
        '''
        Remove link from current chain.  Link being removed must be head or tail link, otherwise error.
        @param link: Link to be removed
        @return: nothing
        '''
        #find at head or tail
        link_cells = [link.node_1, link.node_2]
        self.loop = False
        if len(self.links) == 1:
            self.links = []
            self.head = None
            self.tail = None
            self.head_cell = None
            self.tail_cell = None
            self.loop = False
        elif link == self.head:
            #remove from head
            self.links = self.links[1:]
            self.head = self.links[0]
            self.head_cell = not_cell(self.head_cell, link_cells)
        elif link == self.tail:
            #remove from tail
            self.links = self.links[:-1]
            self.tail = self.links[-1]
            self.tail_cell = not_cell(self.tail_cell, link_cells)
        else:
            raise ValueError('Trying to remove link from XChain that is not head or tail link')

        # TODO Chain can have method for checking rules and clearing hints

    def rules(self):
        if not self.loop:
            raise ValueError('Trying to run rules on XCycle Chain that is not a loop')
        if len(self.links) % 2 == 0 and (self.head.type == 'Strong' or self.tail.type == 'Strong'):
            # Execute Rule 1
            print 'Found XCycle Chain Rule 1:'
            # return True if hint(s) cleared, otherwise False
            # find all segments included in chain and all cells to protect
            segs = []
            protect_cells = []
            hint = self.head.hint
            cell = self.head_cell
            for link in self.links:
                if link.type == 'Weak':
                    for seg in cell.segs:
                        if seg not in segs and seg in link.node_1.segs and seg in link.node_2.segs:
                            segs.append(seg)
                for cell in link.cells:
                    if cell not in protect_cells:
                        protect_cells.append(cell)
            # call for change
            change = False
            for seg in segs:
                change = seg.clear_these_hints([hint],protect_cells,notCells=True) or change
            return change

        elif self.head.type == 'Weak' and self.tail.type == 'Weak':
            # Execute Rule 3 - cell at end, can eliminate hint of this link
            #  return True if hint(s) cleared, otherwise False
            print 'Found XCycle Chain Rule 3:'
            if self.head_cell != self.tail_cell:
                raise ValueError('Not a loop')
            self.head_cell.clearHints([self.head.hint])
            return True

        elif len(self.links) % 2 == 1:
            rule_two = False
            previous = None
            for link in self.links:
                if link.type == 'Strong' and previous == 'Strong':
                    rule_two = True
                    for cell in link.cells:
                        if cell in previous.cells:
                            rule_two_cell = cell
                    previous = link.type
            if self.head.type == 'Strong' and self.tail.type == 'Strong':
                rule_two = True
                rule_two_cell = self.head_cell
            if rule_two:
                # Execute Rule 2
                # Return True if hint(s) cleared, otherwise False
                print 'Found XCycle Chain Rule 2:'
                print 'Setting answer ' + str(self.hint + 1) + ' in cell ' + str(rule_two_cell)
                rule_two_cell.setAnswer(self.hint)
                return True
            return False

class Game(object):

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

    def inString(self):
        sol = ''
        for cell in self.cells:
            if cell.answer == None:
                sol = sol + str(0)
            else:
                sol = sol + str(cell.answer + 1)
        return sol

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

    def solve_naked_sets(self):
        for setSize in range(2,4):
            print 'Checking for naked sets size', setSize
            for group in self.segs:
                for seg in group:
                    if seg.solve_naked_sets(setSize):
                        return True
        return False

    def solve_hidden_sets(self):
        """
        Look for hidden sets in this segment, sets of hints that are contained within a set of cells that
        are equal in size to the hint count (e.g. 3 cells with 3 hints, not in any of the other cells).  If
        true, clear all other hints in these same cells.
        @return: True if any hints were cleared, otherwise False
        """
        self.printHints(False)
        for setSize in range(2,5):
            print 'Checking for hidden sets size ', setSize
            for group in self.segs:
                for seg in group:
                    if seg.solve_hidden_sets(setSize):
                        return True
        return False

    def solve_pointing_sets(self):
        """
        Within a square, find two or three cells with the same hint that are in the same row or column
        If found, clear that hint in all cells that are NOT in the cell set found
        @return: True if hints were cleared, otherwise false
        """
        print 'Checking for pointing sets'
        change = False
        for square in self.sqrs:
            pairSets = square.find_pointing_pair()
            for row,col,sqr,cells,hint in pairSets:
                if row != None:
                    change = row.clear_these_hints([hint],cells,notCells=True) or change
                elif col != None:
                    change = col.clear_these_hints([hint],cells,notCells=True) or change
        return change

    def box_line_reduction(self):
        """
        Within a row or column, find two or three cells with a hint in the same square and only in that square
        If found, clear that hint in all cells in the square not in the found set.
        @return: True if hints were cleared, otehrwise False
        """
        print 'Checking box line reductions'
        change = False
        segs = self.rows + self.cols
        change = False
        for seg in segs:
            pairSets = seg.find_pointing_pair()
            for row,col,sqr, cells,hint in pairSets:
                change = sqr.clear_these_hints([hint],cells,notCells=True) or change
        return change

    def solve_xwings(self):
        """
        Find x-wings pairs, clear any hints eliminated by x-wing pair
        @return: True if any hints were deleted, otherwise False
        """
        def this_xwing(segs, hint):
            # find cells with these 2 hints
            row_set = []
            col_set = []
            cell_set = []
            change = False
            for seg in segs:
                for cell in seg.cells:
                    if cell.hints[hint]:
                        if cell.row not in row_set:
                            row_set.append(cell.row)
                        if cell.col not in col_set:
                            col_set.append(cell.col)
                        cell_set.append(cell)
            if len(row_set) == 2 and len(col_set) == 2:
                # OK we have an xWing set, now do clears.
                # cell_set is protected set
                # now have to know if we were working on rows or columns.  hmm
                # OK, now find segSet opposite the set we are working on
                if segs[0] in self.rows:
                    clear_segs = col_set
                else:
                    clear_segs = row_set
                for seg in clear_segs:
                    change = seg.clear_these_hints([hint],cell_set,notCells=True) or change
            return change

        def solve_xwing_set(segSet):
            change = False
            for hint in range(9):
                xwing_set = []
                for set in segSet:
                    if set.hints_in_seg(hint) == 2:
                        xwing_set.append(set)
                change = all_combo(xwing_set,2,lambda set: this_xwing(set, hint)) or change
            return change

        segs = [self.rows, self.cols]
        change = False
        for segSet in segs:
            change = solve_xwing_set(segSet) or change
        return change

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

    def cell_pairs(self):
        """
        find all cell pairs in game where the segment has only two cells for any given hint
        @return: deduped cell pairs in the form[[cell1, cell2],[cell3,cell4],...]
        """
        segs = self.rows + self.cols + self.sqrs
        pairs_with_hint = hint_count_sets(segs, None, 2)
        pair_list = []
        for pair_set in pairs_with_hint:
            hint,pairs = pair_set
            pair_list = pair_list + pairs
        pairs2 = dedupe_pairs(pair_list)
        return pairs2

    def cell_pairs_by_hint(self):
        """
        Find all cell pairs in the game where the segment (row, col, sqr) has only two cells
        for any given hint
        @return: cell pairs in the form [(hint,[cell1, cell2],[cell3, cell4],...),( ...)]
        """
        segs = self.rows + self.cols + self.sqrs
        # find all segments where a hint shows up only twice
        pairs = hint_count_sets(segs, None, 2)
        # remove duplications from squares
        pairs2 = dedupe_pairs_with_hint(pairs)
        return pairs2

    def simpleColoring(self):
        print 'Using simple coloring to check color rules'
        change = False
        pairs = self.cell_pairs_by_hint()
        chains = create_chains(pairs)
        for chain in chains:
            change = chain.rule_two() or change
            change = chain.rule_four() or change
            change = chain.rule_five() or change
        return change

    def yWings(self):
        """
        Look for yWing combinations.  Clear hints as dictated.
        @return: True if hints were cleared, False otherwise
        """
        print 'Checking for yWings'
        change = False
        for cell in self.cells:
            if cell.countHints() == 2:
                visible_cells = find_visible_cells(cell)
                visible_cells_two_hints = find_twos(visible_cells)
                # find visible cells that have one matching hint with lead cell
                cell_set = []
                for hint in cell.true_hints():
                    for match_cell in visible_cells_two_hints:
                        if hint in match_cell.true_hints():
                            cell_set.append(match_cell)
                # find pair sets that have a matching other hint
                pairSet = find_ywing_set(cell,cell_set)
                if len(pairSet) > 0:
                    print 'Found yWing',cell, pairSet
                    for (pair, hint) in pairSet:
                        common = find_common_cells(find_visible_cells(pair[0]),find_visible_cells(pair[1]))
                        for cellF in common:
                            if cellF != cell and cellF.hints[hint]:
                                cellF.hints[hint] = False
                                print 'Clearing hint', hint, 'in', cellF
                                return True
        return False

    def swordfish(self):
        """
        Implements swordfish strategy
        @return: True if hints were changed, otherwise False
        """
        # search segment set (e.g. rows) in groups of three
        # for each segment in the set, count the hints, should be 2 or 3
        # if we have three segments with 2 or 3 hints, collect up the 'rows' and 'columns'
        # if len(rows) and len(cols) is 2 or 3 then we have an xwing or a swordfish
        # clear hints as needed

        def segs_with_hint_count(hint, count, segs):
            """
            Search through a group of segments, find those segments where the count of 'hint' in its cells
             is less than or equal to 'count', and return those segments as a list
            @param hint: hint we are counting
            @param count: count limit
            @param segs: list of segments to search
            @return: list of segments with count or fewer 'hint'
            """
            returnSet = []
            for seg in segs:
                if seg.hints_in_seg(hint) <= count:
                    returnSet.append(seg)
            return returnSet

        def check_if_swordfish(segSet, hint):
            """
            Check input segment set to see if it is an xWing or swordfish set based on length of set
            Clear hints as appropriate in remainder of game
            @param segSet: list of segments e.g. [row0, row1, row2]
            @return: True if changes were made, False otherwise
            """
            set_len = len(segSet)
            # sets are pre-qualified to have right hint count
            # collect up rows, cols and cells
            change = False
            row_set = []
            col_set = []
            cell_set = []
            for seg in segSet:
                for cell in seg.cells:
                    if cell.hints[hint]:
                        if cell.row not in row_set:
                            row_set.append(cell.row)
                        if cell.col not in col_set:
                            col_set.append(cell.col)
                        cell_set.append(cell)
            if len(row_set) == 3 and len(col_set) == 3:
                # we have a swordfish set
                if segSet[0] in self.rows:
                    clear_set = col_set
                else:
                    clear_set = row_set
                for seg in clear_set:
                    change = seg.clear_these_hints([hint], cell_set, notCells=True) or change
            return change

        change = False
        segSets = [self.rows, self.cols]
        for segSet in segSets:
            for hint in range(9):
                segs_to_search = segs_with_hint_count(hint, 3, segSet)
                change = all_combo(segs_to_search,3,lambda set: check_if_swordfish(set, hint)) or change
        return change

    def xy_chain(self):
        '''
        Find XY chains & clear pincered cell hint. Look for common hint in two-hint cells, with visibility to
        clearable hint in pincered cell, then see if they can be connected with a chain.  Will limit the tries to
        those that are useful and to the hint that matters.
        @return: True if a hint was cleared, otherwise False
        '''
        def find_visible_for_chain(set, hint, possibles):
            '''
            Recursive routine to find cells in game where two cells in input set have visibility to a third
            cell with the hint set true, to be returned as a pair plus the visible cell ([cell1,cell2],vis_cell, hint)
            @param set: list of cells to be evaluated in pairs
            @param hint: hint that is true for each cell in this set and must be true in visible cells
            @param possibles: list of cell pairs from set and visible cell that may be an xy-chain candidate
            @return: possibles
            '''
            if len(set) < 2:
                return possibles  # end of the recurse, return
            lead = set[0]
            vis_set_lead = find_visible_cells(lead)
            for second in set[1:]:
                vis_set_second = find_visible_cells(second)
                vis_set_common = find_common_cells(vis_set_lead, vis_set_second)
                # find cells that have hint of interest
                vis_with_hint = []
                for cell in vis_set_common:
                    if cell.hints[hint] and cell != lead and cell != second:
                        vis_with_hint.append(cell)
                # OK, now have cells with hint visible to both, do we have one or more?
                for vis in vis_with_hint:
                    possibles.append(([lead, second], vis, hint))
            return find_visible_for_chain(set[1:], hint, possibles)

        def xy_chain_exists(set):
            '''
            Evaluate each set to see if an XY chain can be built between them
            @param set: ([cell1, cell2], vis_cell, hint) # we don't need vis_cell here ..
            @return: True if an XY chain exists, otherwise False
            '''
            lead = set[0][0]
            tail = set[0][1]
            vis_cell = set[1]
            hint = set[2]  # this is the XY-chain end hint
            print 'Testing xy-chain ' + str(lead) + ' to ' + str(tail) + ' hint ' + str(hint)
            if hint not in lead.true_hints():
                raise ValueError
            if hint not in tail.true_hints():
                raise ValueError
            next_hint = find_other_hint(lead, hint)
            chain = [lead]
            if build_chain(chain, tail, next_hint, vis_cell, hint):
                # If we get here we have a pair that has visibility to a hint that can be cleared
                #  and we know we can build an XY chain between the pair
                #  so now we can clear that hint
                # vis_cell.hints[hint] = False
                return True
            return False

        def build_chain(chain, tail, last_hint, vis_cell, chain_hint):
            '''
            Try to build an XY chain from lead to tail
            @param lead: first cell
            @param tail: last cell, trying to reach this one
            @param last_hint: hint at the end of the chain
            @param two_hint_cells: list of cells in game with only two hints set
            @return: True if a chain exists, otherwise False
            '''
            # TODO this set below should be a separate recursive routine
            #   Input is lead, tail, last_hint, two_hint_cells
            chain = chain[:]
            # find cells visible to lead:
            vis_cells = find_visible_cells(chain[-1])
            # reduce list to those with the right hint set and not in chain
            vis_with_hint = []
            for cell in vis_cells:
                if cell.hints[last_hint] and cell not in chain and cell != vis_cell and cell.countHints() == 2:
                    vis_with_hint.append(cell)
            # choose next in chain (build chain to eliminate looping)
            for cell in vis_with_hint:
                if cell == tail and last_hint != chain_hint:
                    return True
                else:
                    # chain.append(cell)
                    # last_hint = find_other_hint(cell, last_hint)
                    if build_chain(chain + [cell], tail, find_other_hint(cell, last_hint), vis_cell, chain_hint):
                        return True
            return False
            # determine next hint
            # recurse, looking for tail cell

        def find_other_hint(cell, hint):
            '''
            Assumes cell has two true hints.  One is passed in.  Return the other one
            @param cell: cell object with two true hints
            @param hint: hint we already know, integer range(9)
            @return: true_hint, value of second true hint, integer range(9)
            '''
            # TODO simple function to find other true hint, return hint
            for true_hint in cell.true_hints():
                if true_hint != hint:
                    return true_hint
            raise ValueError('Could not find true hint other than hint passed to function')
        # find 2-hint cells
        two_hint_cells = find_twos(self.cells)
        # find pairs of cells with visibility to hints not cleared, by hint
        for hint in range(9):
            cell_set_one_hint = []
            for cell in two_hint_cells:
                if cell.hints[hint]:
                    cell_set_one_hint.append(cell)
            return_set = []
            possibles = find_visible_for_chain(cell_set_one_hint, hint, return_set)
            # OK, now we have two cells and a visible cell (a whole list of them)
            # Can we build an XY chain between the two cells, with 'hint' open at each end?
            for set in possibles:
                if(xy_chain_exists(set)):
                    set[1].hints[set[2]] = False
                    return True
        return False

    def x_cycle(self):
        '''
        Find X-Cycles, hints in visible cells, return True if hints cleared
        @return:
        '''
        def cell_in_set(cell, pair, set):
            for pair2 in set:
                if pair2 == pair: continue
                if cell in pair2:
                    return True
            return False

        def check_sets(open_cell, strong_set, weak_set):
            '''
            Determine if there is a link in strong_set or weak_set that has open_cell on one end of the link
            @param open_cell:
            @param strong_set:
            @param weak_set:
            @return: set of matching links if one exists, False otherwise
            '''
            return_set = []
            for s_link in strong_set:
                if open_cell == s_link.node_1 or open_cell == s_link.node_2:
                    return_set.append(s_link)
            for w_link in weak_set:
                if open_cell == w_link.node_1 or open_cell == w_link.node_2:
                    return_set.append(w_link)
            if len(return_set) > 0:
                return return_set
            return False

        def build_x_cyc_chain(strong_set, weak_set, up_chain=XChain()):
            def copy_xchain(xchain_old):
                xchain_new = XChain()
                xchain_new.links = xchain_old.links
                xchain_new.head = xchain_old.head
                xchain_new.tail = xchain_old.tail
                xchain_new.head_cell = xchain_old.head_cell
                xchain_new.tail_cell = xchain_old.tail_cell
                xchain_new.hint = xchain_old.hint
                return xchain_new
            global depth
            depth += 1
            # print 'Entering, Depth: ' + str(depth),
            # up_chain.str_links()
            change = False
            chain = copy_xchain(up_chain)
            if len(chain.links) == 0:
                chain.add_link(strong_set[0], 'Tail')
                strong_set = strong_set[1:]
            #extend on head or tail?
            if len(chain.links) == 1:
                end_links = [(chain.tail, chain.tail_cell, 'Tail')]
            else:
                end_links = [(chain.tail, chain.tail_cell, 'Tail'), (chain.head, chain.head_cell, 'Head')]
            for tup in end_links:
                end_link = tup[0]
                # find free link
                open_cell = tup[1]
                end = tup[2]
                # if last link is strong, we don't care about previous link, find strong or weak link next
                if end_link.type == 'Strong':
                    found_links = check_sets(open_cell, strong_set, weak_set)
                elif end_link.type == 'Weak':
                    found_links = check_sets(open_cell, strong_set, [])
                else:
                    found_links = False
                if found_links:
                    for found_link in found_links:
                        chain.add_link(found_link, end)
                        if found_link.type == 'Strong':
                            strong_set_local = []
                            for link in strong_set:
                                if link != found_link:
                                    strong_set_local.append(link)
                            weak_set_local = weak_set[:]
                        elif found_link.type == 'Weak':
                            weak_set_local = []
                            for link in weak_set:
                                if link != found_link:
                                    weak_set_local.append(link)
                            strong_set_local = strong_set[:]
                        # Now check for loop
                        if chain.loop:
                            change = chain.rules()
                        # recurse
                        if change:
                            return True
                        elif len(strong_set_local) == 0 and len(chain.links) == 0:
                            continue
                        else:
                            change = build_x_cyc_chain(strong_set_local, weak_set_local, chain)
                        chain.remove_link(found_link)
            if len(chain.links) == 1:
                # strong_set.pop(0)
                chain.remove_link(chain.links[0])
                up_chain = XChain()
                if len(strong_set) > 0:
                    change = build_x_cyc_chain(strong_set, weak_set, chain)
            depth -= 1
            # print 'Exit, Depth: ' + str(depth),
            # up_chain.str_links()
            return change

        def build_x_cycle(strong_set_tuple, weak_set):
            hint = strong_set_tuple[0]
            strong_set = strong_set_tuple[1]
            # find subset of strong set that has a match in either strong or weak set for both ends
            strong_set_links = []
            for s_pair in strong_set:
                if (cell_in_set(s_pair[0], s_pair, strong_set) or cell_in_set(s_pair[0], s_pair, weak_set)) and \
                    (cell_in_set(s_pair[1], s_pair, strong_set) or cell_in_set(s_pair[1], s_pair, weak_set)):
                    strong_set_links.append(XChain_Link('Strong', hint, s_pair))
            # find subset of weak set that has a match in either strong or weak set for both ends
            weak_set_links = []
            # weak links have to be connected to a strong link on at least one end
            for w_pair in weak_set:
                if (cell_in_set(w_pair[0], w_pair, strong_set)) and \
                    (cell_in_set(w_pair[1], w_pair, strong_set) or cell_in_set(w_pair[1], w_pair, weak_set)) or \
                    (cell_in_set(w_pair[1], w_pair, strong_set)) and \
                    (cell_in_set(w_pair[0], w_pair, strong_set) or cell_in_set(w_pair[0], w_pair, weak_set)):
                    if w_pair not in strong_set:
                        weak_set_links.append(XChain_Link('Weak', hint, w_pair))
            chain = XChain()
            return build_x_cyc_chain(strong_set_links, weak_set_links, chain)

        def find_weak_links(pair_set, hint):
            lead = pair_set[0]
            weak_links = []
            if len(pair_set) < 2:
                return weak_links
            for second in pair_set[1:]:
                # check both components of lead against second for common row/col/sqr
                for lead_cell in lead:
                    for second_cell in second:
                        if (lead_cell.row == second_cell.row or \
                            lead_cell.col == second_cell.col or \
                            lead_cell.sqr == second_cell.sqr) and lead_cell != second_cell:
                            weak_links.append(sorted([lead_cell, second_cell]))
            return weak_links + find_weak_links(pair_set[1:], hint)

        def find_weak_links2(s_pairs, hint):
            weak_set = []
            for pair in s_pairs:
                for cell in pair:
                    # find other cells in row, col, sqr with same hint
                    weak_link_set = [cell.row.cells_with_hint(hint), cell.col.cells_with_hint(hint), cell.sqr.cells_with_hint(hint)]
                    for set in weak_link_set:
                        if set == False: continue
                        for cell2 in set:
                            if cell != cell2:
                                new_link = sorted([cell, cell2])
                                if new_link not in weak_set:
                                    weak_set.append(new_link)
            return weak_set

        print 'Checking X-Cycles'
        # find strong links
        # pairs come sorted by using dedupe in cell_pairs_by_hint method
        strong_pairs = self.cell_pairs_by_hint()
        # do one hint at a time
        for strong_set in strong_pairs:
            if len(strong_set[1]) < 2: continue
            hint = strong_set[0]
            pairs = strong_set[1]
            # find weak links
            weak_set_untested = find_weak_links2(pairs, hint)
            # eliminate those that are actually strong links
            weak_set = []
            for weak_pair in weak_set_untested:
                if weak_pair not in strong_set[1]:
                    weak_set.append(weak_pair)
            if len(weak_set) > 1:
                # do something interesting
                global depth
                depth = 0
                change = build_x_cycle(strong_set, weak_set)
                if change:
                    return True
        return False

def create_chains(pairs):
    # create chains
    """
    Take a set of cell pairs, create nodes of a chain and color the chains.  Return a list
      of colored chains
    @param pairs: list of cell pairs in the form [(hint,[[cell1, cell2],[cell3, cell4]...]),(hint, [[...]
    @return: list of colored chains in the form[chain,chain,chain ...]
    """
    # iterate from here over the 9 sets in 'pairs' and for each one create chains
    chainSet = []
    for hintPairSet in pairs:
        chains = create_simple_chain(hintPairSet)
        chainSet = chainSet + chains
    for chain in chainSet:
        chain.color()
    return chainSet

def create_medusa_chains(pairs):
    '''
    Create a chain using all hints for Medusa strategy
    @param pairs: list of cell pairs in the form [(hint,[[cell1, cell2],[cell3, cell4]...]),(hint, [[...]
    @return: list of colored chains in the form[chain,chain,chain ...]
    '''

def create_simple_chain(hintPairSet):
    """
    Takes a list of cell pairs as input, all with the same hint, and creates the chain links
    First part builds a dictionary that creates a node for each cell, and links that node
     to each other node where the chain connects
    Nodes are then extracted from the dictionary into a list
    Chains are then built from the node list and put into a list of chains, which is returned
    @param pairs: in the form (hint, [cell1, cell2],[cell3, cell4] ...)
    @return: chains: in the form [chain1,chain2,chain3,...]
    """
    chainDict = {}
    hint, cellSet = hintPairSet
    for cellPair in cellSet:
        for cell in cellPair:
            if cell not in chainDict:
                chainDict[cell] = ChainNode(cell)
        chainDict[cellPair[0]].addLink(chainDict[cellPair[1]])
        chainDict[cellPair[1]].addLink(chainDict[cellPair[0]])
    # Convert to a list of nodes
    nodeSet = []
    for cell in chainDict:
        nodeSet.append(chainDict[cell])
    # now use this nodeSet (set of nodes) to build the chains
    # take first node in the list, follow and find the set that constitute a chain, then
    #  remove those nodes from the nodeSet
    chainSet = []
    while len(nodeSet):
        newChain = Chain(hint, nodeSet[0])
        chainSet.append(newChain)
        newNodeSet = []
        for node in nodeSet:
            if node not in newChain.nodes:
                newNodeSet.append(node)
        nodeSet = newNodeSet
    return chainSet

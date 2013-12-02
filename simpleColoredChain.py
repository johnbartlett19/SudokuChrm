#/bin/python
import copy
from yWings00 import findVisibleCells
from yWings00 import findCommonCells

class ChainNode(object):
    def __init__(self, cell):
        self.cell = cell
        self.color = None
        self.links = []
    def __repr__(self):
        return 'ChNode-' + str(self.cell) + '-' + str(self.color)
    def addLink(self, node):
        self.links.append(node)

#def twoHintSegs(hint, game):
#    twins = []
#    segs = ['Rows', 'Cols', 'Squares']
#    for segType in segs:
#        for segment in game[segType]:
#            hintCnt = 0
#            cellSet = []
#            for cell in segment.cells:
#                if cell.hints[hint]:
#                    hintCnt += 1
#                    cellSet.append(cell)
#            if hintCnt == 2:
#                twins.append(cellSet)
#    twinsClean = []
#    for pair in twins:
#        pairSwap = (pair[1],pair[0])
#        if pair not in twinsClean and pairSwap not in twinsClean:
#            twinsClean.append(pair)
#    return twinsClean

def findChain(node, chainSet):
    chainSet.append(node)
    for link in node.links:
        if link not in chainSet:
            findChain(link, chainSet)
    return chainSet
    

def createChains(pairs):
    chainDict = {}
    for pair in pairs:
        for cell in pair:
            try:
                node = chainDict[cell]
            except:
                node = ChainNode(cell)
                chainDict[cell] = node
        chainDict[pair[0]].addLink(chainDict[pair[1]])
        chainDict[pair[1]].addLink(chainDict[pair[0]])
    # Convert to a list of nodes
    nodeSet = []
    for cell in chainDict:
        nodeSet.append(chainDict[cell])
    returnSet = []
    while len(nodeSet):
        node = nodeSet[0]
        chainSet = []
        findChain(node, chainSet)
        returnSet.append(chainSet)
        newNodeSet = []
        for node in nodeSet:
            if node not in chainSet:
                newNodeSet.append(node)
        nodeSet = newNodeSet
    return returnSet
            
def allColored(chain):
        for node in chain:
            if node.color == None:
                return False
        return True

def colorChain(node, chain, last='Blue'):
    if node.color != None:  # color this one
        raise ValueError ('Node should be uncolored')
    if last == 'Blue':
        node.color = 'Red'
    elif last == 'Red':
        node.color = 'Blue'
    for nodeLink in node.links:  # follow the links
        if nodeLink.color == None:
            colorChain(nodeLink, chain, node.color)              


''' Rules have to be run on single chains.  Need to separate out chains
    after a run of coloring and provide multiple chains back where needed'''

'''    Rule 2: Can't be two hints with the same color in the same segment,
        delete all '''
def nodeComp(node1,node2):
    #return true if two nodes are in a common segment
    if node1.cell.row == node2.cell.row:
        return True
    elif node1.cell.col == node2.cell.col:
        return True
    elif node1.cell.sqr == node2.cell.sqr:
        return True
    return False

''' Rule 2 - if two cells with the same color are found in the same segment, the hint
     in those two cells can be removed  '''
def ruleTwo(chain):
    if len(chain) < 2:
        return False
    for node in chain[1:]:
        if nodeComp(chain[0],node) and chain[0].color == node.color:
            print 'Chain[0]', chain[0], 'Node', node
            raise ValueError ('Simple Colored Chain Rule Two found, still not implemented')
            return True
        return ruleTwo(chain[1:])

'''    5) Rule 4: If both colors appear in a segment, no other cells in that
        segment can have the same hint '''
def ruleFour(chain):
    if len(chain) < 2:
        return False
    for node in chain[1:]:
        if nodeComp(chain[0],node) and chain[0].color != node.color:
            return (chain[0], node)
    return ruleFour(chain[1:])

'''    6) Rule 5: Two colors elsewhere.  If a cell has visibility to two colored
        cells of different colors, it can't have that hint
'''


def findHintCells(hint, cellSet):
    """
    find all cells in cellSet that have the hint 'hint' set and return a set of cells
    """
    returnSet = []
    for cell in cellSet:
        if cell.hints[hint]:
            returnSet.append(cell)
    return returnSet


def ruleFiveCombo(chain, common, twoHintCells):
    if len(chain) < 2:
        return common
    for node in chain[1:]:
        if chain[0].color != node.color:
            cellSet1 = findVisibleCells(chain[0].cell, twoHintCells)
            cellSet2 = findVisibleCells(node.cell, twoHintCells)
            commVis = findCommonCells(cellSet1, cellSet2)
            for cell in commVis:
                common.append(cell)
    return ruleFiveCombo(chain[1:], common, twoHintCells)

def ruleFive(chain, twoHintCells):
    common = []
    visible = ruleFiveCombo(chain, common, twoHintCells)
    chainCellSet = []
    for node in chain:
        chainCellSet.append(node.cell)
    print chainCellSet
    returnSet = []
    print 'Visible', visible
    print 'ChainCellSet', chainCellSet
    for cell in visible:
        if cell not in chainCellSet:
            returnSet.append(cell)
    if len(returnSet) > 0:
        print 'ReturnSet', returnSet
        raise ValueError ('Simple Colored Chain Rule Four found, not implemented')
    returnSet

def printChain(chain):
    for node in chain:
        print node
        for link in node.links:
            print '\t',link
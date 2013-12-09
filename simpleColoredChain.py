#/bin/python
import copy
from yWings import findVisibleCells, findCommonCells
#from classes import Chain

# class ChainNode(object):
#     def __init__(self, cell):
#         self.cell = cell
#         self.color = None
#         self.links = []
#     def __repr__(self):
#         return 'ChNode-' + str(self.cell) + '-' + str(self.color)
#     def addLink(self, node):
#         self.links.append(node)

# def findChain(node, chain):
#     chain.addLink(node)
#     for link in node.links:
#         if link not in node.links:
#             findChain(link, chain)
#     return chain

# def createChains(hint, pairs):
#     """
#     Takes a list of cell pairs as input, all with the same hint, and creates the chain links
#     First part builds a dictionary that creates a node for each cell, and links that node
#      to each other node where the chain connects
#     Nodes are then extracted from the dictionary into a list
#     Chains are then built from the node list and put into a list of chains, which is returned
#     @param pairs: in the form [[cell1, cell2],[cell3, cell4] ...]
#     @return: chains: in the form [[chain],[chain],...]
#     """
#     chainDict = {}
#     for pair in pairs:
#         for cell in pair:
#             try:
#                 node = chainDict[cell]
#             except:
#                 node = ChainNode(cell)
#                 chainDict[cell] = node
#         chainDict[pair[0]].addLink(chainDict[pair[1]])
#         chainDict[pair[1]].addLink(chainDict[pair[0]])
#     # Convert to a list of nodes
#     nodeSet = []
#     for cell in chainDict:
#         nodeSet.append(chainDict[cell])
#     # now use this nodeSet (set of nodes) to build the chains
#     returnSet = [] # to collect up the chain objects
#     # take first node in the list, follow and find the set that constitute a chain, then
#     #  remove those nodes from the nodeSet
#     while len(nodeSet):
#         chain = Chain(hint)
#         chain.nodes = findChain(nodeSet[0])
#         returnSet.append(chain)
#         newNodeSet = []
#         for node in nodeSet:
#             if node not in chain.nodes:
#                 newNodeSet.append(node)
#         nodeSet = newNodeSet
#     return returnSet
            
def allColored(chain):
        for node in chain:
            if node.color == None:
                return False
        return True

def nodeComp(node1,node2):
    """
    Compares two nodes, returns true if they are in a common segment
    @param node1: Node for comparison
    @param node2: Node for comparison
    @return: True if both nodes are in the same row, col or sqr, otherwise False
    """
    if node1.cell.row == node2.cell.row:
        return node1.cell.row
    elif node1.cell.col == node2.cell.col:
        return node1.cell.col
    elif node1.cell.sqr == node2.cell.sqr:
        return node1.cell.sqr
    return False

# def ruleTwo(chain):
#     """
#     Rule 2 - if two cells with the same color are found in the same segment, the hint in those two cells
#      can be removed.  This routine takes a chain as input, clears the hints if the rule is true, and
#      returns True if changes were made, otherwise False
#     @param chain: chain to be checked against Rule 2
#     @return: True if hints were cleared, otherwise False
#     """
#     if len(chain) < 2:
#         return False
#     for node in chain[1:]:
#         if nodeComp(chain[0],node) and chain[0].color == node.color:
#             print 'Chain[0]', chain[0], 'Node', node
#             raise ValueError ('Simple Colored Chain Rule Two found, still not implemented')
#             return True
#         return ruleTwo(chain[1:])
#
# def ruleFour(chain):
#     """
#     Rule 4 - If both colors appear in the same segment, no other cells in that segment can have the same hint.
#       This routine takes a chain as input, determines if two of the chain cells are in a common segment, and
#       if true, clears the hint in the other cells of that segment.
#     @param chain: Chain to be checked against rule 4
#     @return: True if hints were changed, otherwise False
#     """
#     if len(chain) < 2:
#         return False
#     for node in chain[1:]:
#         if nodeComp(chain[0],node) and chain[0].color != node.color:
#             return (chain[0], node)
#     return ruleFour(chain[1:])

def findHintCells(hint, cellSet):
    """
    find all cells in cellSet that have the hint 'hint' set and return a set of cells
    @param hint:
    @param cellSet:
    """
    returnSet = []
    for cell in cellSet:
        if cell.hints[hint]:
            returnSet.append(cell)
    return returnSet

# def ruleFiveCombo(chain, common, twoHintCells):
#     """
#
#     @param chain:
#     @param common:
#     @param twoHintCells:
#     @return:
#     """
#     if len(chain) < 2:
#         return common
#     for node in chain[1:]:
#         if chain[0].color != node.color:
#             cellSet1 = findVisibleCells(chain[0].cell, twoHintCells)
#             cellSet2 = findVisibleCells(node.cell, twoHintCells)
#             commVis = findCommonCells(cellSet1, cellSet2)
#             for cell in commVis:
#                 common.append(cell)
#     return ruleFiveCombo(chain[1:], common, twoHintCells)
#
# def ruleFive(chain, twoHintCells):
#     """
#     Rule 5 - If a cell not in the chain has visibility to two different colored cells of the chain,
#      the hint in that cell can be removed.  This routine checks the whole game for cells that have visibility
#      to this chain, and clears the hint if the rule is true
#     @param chain:
#     @param twoHintCells:
#     @return: True if hints were changed, otherwise False
#     """
#     common = []
#     visible = ruleFiveCombo(chain, common, twoHintCells)
#     chainCellSet = []
#     for node in chain:
#         chainCellSet.append(node.cell)
#     print chainCellSet
#     returnSet = []
#     print 'Visible', visible
#     print 'ChainCellSet', chainCellSet
#     for cell in visible:
#         if cell not in chainCellSet:
#             returnSet.append(cell)
#     if len(returnSet) > 0:
#         print 'ReturnSet', returnSet
#         raise ValueError ('Simple Colored Chain Rule Five found, not implemented')
#     returnSet

def printChain(chain):
    for node in chain:
        print node
        for link in node.links:
            print '\t',link
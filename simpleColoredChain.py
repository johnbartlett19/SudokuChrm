#/bin/python
import copy
from yWings import find_visible_cells, find_common_cells

# TODO Add doc strings to this top function.  Is this used at all?  Eliminate?
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

def printChain(chain):
    for node in chain:
        print node
        for link in node.links:
            print '\t',link
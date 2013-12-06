
#/bin/python
import string, copy
from yWings import *
from simpleColoredChain import *
from classes import *
from basics import *

def solveLoop(game):
    change = True
    while change:
        game.clearHints()
        change = False
        if game.solveSingle():
            change = True
        elif game.check():
            break
        elif game.solveSingleRCS():
            change = True
        elif game.solveNakedSets():
            change = True
        elif game.solveHiddenSets():
            change = True
        elif game.solvePointingSets():
            change = True
        elif game.boxLineReduction():
            change = True
        elif game.solveXwings():
            change = True
        #elif game.simpleColoring():
        #    change = True
    #    elif solveYwings(game):
    #        chafdnge = True
    #return change
    #if game.check():
    #    change = False

inString = '800900500020037000100400070400000050092673410010000006040009003000720090009006005' #solves with single RCS
inString = '   7    6 5  92  71    6     31 4 7 86     59 7 9 83     6    55  82  4 2    9   '
inString = '39 5         1  541  6   8 9 4   3 6         2 6   7 8 1 9 6   57  4         8 47'
inString = '      15  597  4  8 3     27 2  5  4   2 1   5  9  8 66     5 1  5  829  91      ' #solves with Naked Sets
inString = '000007300000003042030280007000020403040000060908030000600049020710600000002100000' #solves with Naked Sets
inString = '000000005100005400057009010004600000230000097000008100060300740002700008300000000' #solves with Naked Sets
inString = '903080000000000180060420000000800700206010905004009000000064010057000000000030804' #solves with Naked Sets
inString = '000800003530002007006005910000004080007000400090600000013200700400900051700008000' #solves with Naked Sets
inString = ' 8 7  2 53 5  67 4         6    73 9 7 6 3 4 5 49    1         1 25  9 38 3  1 5 ' #solves with Naked Sets
inString = '12 5      6  7    784  9     1  69  65 4 1 73  87  4     2  189    3  6      7 32' #solves with pointing sets (does not need hidden sets)
inString = '000705000100000003098000470070569080000080000050173040013000260400000008000306000' #solves with pointing sets and box line reduction
inString = ' 3  2  7 4  1 7  8  8   6    6 8 2     9 2     5 7 8    9   1  6  4 9  5 8  3  9 ' #needs xWings
inString = '800207000500400020010000003080000460000901000025000010400000090060003002000509008'
#inString = '  2 48   8    6     4  23 5 5   7 3 2 7 3 9 8 8 4   2 1 38  7     6    1   97 8  ' # needs simple coloring
#inString = '309000400200709000087000000750060230600904008028050041000000590000106007006000104'

game = Game()
game.setGameStart(inString)
game.printAnswers(True)
print

solveLoop(game)
if game.check():
    print 'Success! - completed puzzle'
else:
    print 'More work to be done!!!'
print
game.printAnswers(True)
print
game.printHints(True)

#openWeb(inString)
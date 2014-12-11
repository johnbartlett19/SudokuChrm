
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
        #game.printHints(True)
        change = False
        if game.solveSingle():
            change = True
        elif game.check():
            break
        elif game.solveSingleRCS():
            change = True
        elif game.solve_naked_sets():
            change = True
        elif game.solve_hidden_sets():
            change = True
        elif game.solve_pointing_sets():
            change = True
        elif game.box_line_reduction():
            change = True
        elif game.solve_xwings():
            change = True
        elif game.simpleColoring():
            change = True
        elif game.yWings():
            change = True
        elif game.swordfish():
            change = True
        elif game.xy_chain():
            change = True
        elif game.x_cycle():
            change = True
    #return change
    #if game.check():
    #    change = False

#inString = '800900500020037000100400070400000050092673410010000006040009003000720090009006005' #solves with single RCS
#inString = '   7    6 5  92  71    6     31 4 7 86     59 7 9 83     6    55  82  4 2    9   '
#inString = '39 5         1  541  6   8 9 4   3 6         2 6   7 8 1 9 6   57  4         8 47'
#inString = '000000150059700400803000002702005004000201000500900806600000501005008290091000000' #solves with Naked Sets
#inString = '000007300000003042030280007000020403040000060908030000600049020710600000002100000' #solves with Naked Sets
#inString = '000000005100005400057009010004600000230000097000008100060300740002700008300000000' #solves with Naked Sets
#inString = '903080000000000180060420000000800700206010905004009000000064010057000000000030804' #solves with Naked Sets
#inString = '000800003530002007006005910000004080007000400090600000013200700400900051700008000' #solves with Naked Sets
#inString = ' 8 7  2 53 5  67 4         6    73 9 7 6 3 4 5 49    1         1 25  9 38 3  1 5 ' #solves with Naked Sets
#inString = '300000000970010000600583000200000900500621003008000005000435002000090056000000001' #solves with Naked Sets
#inString = '000060000000042736006730040094000068000096407607050923100000085060080271005010094' #hidden pair (if naked sets < 4)
#inString = '500620037004890000000050000930000000020000605700000003000009000000000700680570002' #hidden triple (if naked sets < 4)
#inString = '030000010008090000400608000000576940000983520000124000276005190000709000095000470' #hidden quad and pointing sets
#inString = '12 5      6  7    784  9     1  69  65 4 1 73  87  4     2  189    3  6      7 32' #solves with pointing sets (does not need hidden sets)
#inString = '000705000100000003098000470070569080000080000050173040013000260400000008000306000' #solves with pointing sets and box line reduction
#inString = '000903010004000600750000040000480000200000003000052000040000081005000260090208000' # tough box-line reduction example
#inString = ' 3  2  7 4  1 7  8  8   6    6 8 2     9 2     5 7 8    9   1  6  4 9  5 8  3  9 ' #needs xWings
#inString = '800207000500400020010000003080000460000901000025000010400000090060003002000509008'
#inString = '  2 48   8    6     4  23 5 5   7 3 2 7 3 9 8 8 4   2 1 38  7     6    1   97 8  ' #needs simple coloring rule 2
#inString = '8 7 9 6 295286  4 3 6 2 598781934256264     95396 2  46     42112  4698 4 821  65' #needs simple coloring rule 5
#inString = '036210840800045631014863009287030456693584000145672398408396000350028064060450083' #needs simple coloring rule 4 and yWings
#inString = '309000400200709000087000000750060230600904008028050041000000590000106007006000104' #needs yWings
# inString = '900040000000600031020000090000700020002935600070002000060000073510009000000080009' #tough test of yWings
# inString = '409716000610389040070245169000964021004173690196852030960421070030698000040537906' #solves with Hidden Sets & box line reduction & ywing
# inString = '195367248078050369306098157003780590709005006584906710832549671907013025051072900' #needs swordfish
# inString = '080103070000000000001408020570001039000609000920800051030905200000000000010702060' #needs XY chains
# inString = '050030602642895317037020800023504700406000520571962483214000900760109234300240170' #needs swordfish and XY chain
# inString = '092000376010030500300000190930850701000304000200097003689003410523040060147000230' #XY chains from Andrew
# inString = '024100670060070410700964020246591387135487296879623154400009760350716940697040031' #X-Cycle Rule 1 from Andrew
# inString = '000900000008010500300002060007000080000406000010000900020700003005090100006008000' #X-Cycle Rule 2 from PaulsPages.co.uk, requires Grouped X-cycles
inString = '804537000023614085605982034000105870500708306080203450200859003050371208008426507' #X-Cycle Rule 2 from Andrew (turn off other stuff)
# inString = '000800042000001070900002003007000050100030004040000800400900006050200010280006000' # X-Cycle Rule 3 and alternating inference chains from Andrew
game = Game()
game.setGameStart(inString)
#game.printAnswers(True)

solveLoop(game)
if game.check():
    print 'Success! - completed puzzle'
else:
    print 'More work to be done!!!'
print
game.printAnswers(True)
print
game.printHints(True)
open_web(game.inString())
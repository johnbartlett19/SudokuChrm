from classes import *

testStr = [0,1,2,3,4,5,6,7,8,9]

#find_triplet(testStr, 3, addEm)
# TODO Can this be modified to allow me to pass in parameters as well as use local parameters in the function I pass in?

def printEm(list):
    for item in list:
        print item,
    print 'new'

def print_w_label(list,label):
    change = False
    print label,
    for item in list:
        print item,
    print 'end',
    if list == [1,3,5,7,9]:
        change = True
    return change

def print_w_five(list):
    print_w_label(list, 'five')

def all_combo2(theSet, count, function, change=False, preSet=[]):
    # print 'Pre', preSet, 'Set', theSet
    if len(theSet) < count - len(preSet):
        return change
    preSet = preSet[:] + [theSet[0]]
    workSet = theSet[:]
    while len(workSet[1:]) + len(preSet) >= count:
    # preSet.append(theSet[0])
        if len(preSet) == count - 1:  # this is the run test
            for last in theSet[1:]:
                work = preSet + [last]
                change = function(work) or change
            return change
        elif len(preSet) < count-1:
            # print 'Go next level to increase size of preSet'
            change = all_combo2(workSet[1:], count, function, change, preSet) or change # call to get preSet large enough
            asdf = 1
        elif len(preSet) >= count:
            raise ValueError('preSet too large')
        # print 'move to next level'
        #while len(workSet[1:]) + len(preSet) >= count:
        #    all_combo2(workSet[1:], count, function, change, preSet)
        workSet = workSet[1:]
    return all_combo2(theSet[1:], count, function, change, preSet[:-1])

def all_combo3(theSet, count, function, change=False, preSet=[]):
    # build as two routines, one inside the other, both recurse
    # the first one (here) builds the pre-set and iterates through the whole set
    # the second one takes the pre-set and the rest and iterates through the rest
    # print 'Pre', preSet, 'Set', theSet
    if len(theSet) < count - len(preSet):
        return change
    preSet = preSet[:] + [theSet[0]]
    workSet = theSet[:]
    while len(workSet[1:]) + len(preSet) >= count:
    # preSet.append(theSet[0])
        if len(preSet) == count:  # this is the run test
            #run_combos(workSet, count, function, change, preSet)

            for last in theSet[1:]:
                work = preSet + [last]
                change = function(work) or change
            return change
        elif len(preSet) < count-1:
            # print 'Go next level to increase size of preSet'
            all_combo2(workSet[1:], count, function, change, preSet) # call to get preSet large enough
            asdf = 1
        elif len(preSet) >= count:
            raise ValueError('preSet too large')
        # print 'move to next level'
        #while len(workSet[1:]) + len(preSet) >= count:
        #    all_combo2(workSet[1:], count, function, change, preSet)
        workSet = workSet[1:]
    return all_combo2(theSet[1:], count, function, change, preSet[:-1])

def all_combo4(theSet, count, function, preSet=[], change=False):
    if len(theSet)+len(preSet) < count:
        return change
    preSet = preSet[:] + [theSet[0]]
    mySet = theSet[1:]
    if len(preSet) == count:
        change = function(preSet) or change
        print change
        theSet.pop(0)
        return all_combo(mySet, count, function, preSet[:-1],change)
    if len(preSet) < count:
        change = all_combo(mySet, count, function, preSet, change) or change
    return all_combo(theSet[1:], count, function, preSet[:-1], change)

count = 5
label = 'eol'
aa = all_combo(testStr,count, lambda list: print_w_label(list, label))
# aa = all_combo4(testStr, count)
print aa
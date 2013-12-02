
def addList(item, list = []):
    list.append(item)
    return list


aa = addList('a')
print aa
bb = addList('b', aa)
print bb
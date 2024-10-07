def getPagesNumber(order, reverse = False, getCompleteList = False, getUniceList = False):
    order = str(order)
    if getCompleteList:
        getUniceList = False
    else:
        getUniceList = True

    order = order.replace(' ', '')
    order = order.replace(',', ';')
    order = order.replace('--', '-')
    if order == '':
        return []
    elif '-;' in order:
        return []
    elif ';-' in order:
        return []
    elif order[0] in ('-', ';'):
        return []
    elif order[-1] in ('-', ';'):
        return []

    order = order.split(';')
    if '' in order:
        return []

    pages = []
    for i in order:
        if '-' not in i:
            if (getUniceList and int(i) not in pages) or getCompleteList:
                pages.append(int(i))
        else:
            beg, end = i.split('-')
            for j in range(int(beg), int(end) + 1):
                if (getUniceList and j not in pages) or getCompleteList:
                    pages.append(j)

    if reverse:
        pages = pages[::-1]

    return pages

def getPageSet(pages):
    sets = []
    for i in range(len(pages)):
        if pages[i-1] + 1 == pages[i]:
            sets[-1].append(pages[i])
            continue
        sets.append([pages[i]])

    txt = ''
    for s in sets:
        if len(s) == 1:
            txt += '; ' + str(s[0])

        else:
            txt += '; ' + str(s[0]) + '-' + str(s[-1])

    return txt[2:]

if __name__ == '__main__':
    pages_str = '1-12; 14--16; 20; 22'
    pages = getPagesNumber(pages_str)
    print(pages)
    print(getPageSet(pages))

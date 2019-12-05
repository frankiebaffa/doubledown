def arrFind(p,a):
    try:
        return a.index(p)
    except:
        return -1

import re
def regexHas(p,s):
    return len(re.findall(p,s)) > 0

def regexHasOne(p,s):
    return len(re.findall(p,s)) == 1

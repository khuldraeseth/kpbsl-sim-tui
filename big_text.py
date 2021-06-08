#from digits import digits
from chars import chars

def transpose(xss):
    return [list(xs) for xs in zip(*xss)]

def strcat(ss):
    return "".join(ss)

def concat(xss):
    result = []
    for xs in xss:
        result += xs
    return result

def stranspose(ss):
    return [strcat(s) for s in transpose(ss)]

def embiggenLines(s):
    return stranspose(concat([stranspose(chars[c]) for c in s]))

def embiggen(x):
    if type(x) is int:
        return embiggen(str(x))
    return '\n'.join([row[:-1] for row in embiggenLines(x)])

def printBig(x):
    print(embiggen(x))

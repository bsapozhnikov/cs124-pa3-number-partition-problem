from sys import argv, exit
import random

INPUT_LEN = 100

def getArray(filename="ones.txt"):
    inputfile = open(filename, 'r')
    A = []
    for _ in xrange(INPUT_LEN):
        A.append(int(inputfile.readline()))
    return A

### Insert x into A     ###
### Assumes A is sorted ###
def binsert(A, x):
    i,j = 0,len(A)
    while i < j:
        k = (i + j) // 2
        if A[k] == x:
            i = k
            break
        elif A[k] < x:
            i = k + 1
        else:
            j = k
    A.insert(i, x)
    
def kk(A):
    A.sort()
    for _ in xrange(len(A)-1):
        m1 = A.pop()
        m2 = A.pop()
        binsert(A, abs(m1 - m2))
    return A[0]

### Generate and return a random solution  ###
###   represented as a list of +1s and -1s ###
def genSolutionSeq():
    S = []
    for _ in xrange(INPUT_LEN):
        S.append(random.choice([-1,1]))
    return S

def main():
    A = []
    if len(argv) < 2:
        ## print "Usage: python ./kk.py inputfile"
        ## exit(1)
        A = getArray()
    else:
        A = getArray(argv[1])
    print kk(A)
    
main()



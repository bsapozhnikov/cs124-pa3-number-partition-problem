from sys import argv, exit, maxint
import random

INPUT_LEN = 100
NUM_TRIALS = 25000

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

### Generate and return a random prepartition   ###
###   represented as a list of random group ids ###
def genPrepartition():
    P = []
    for _ in xrange(INPUT_LEN):
        P.append(random.randint(0,INPUT_LEN - 1))
    return P

### Repeated Random with solution sequences ###
def rrSeq(A):
    minResidue = maxint
    for _ in xrange(NUM_TRIALS):
        S = genSolutionSeq()
        residue = abs(sum(A[i] * S[i] for i in xrange(INPUT_LEN)))
        minResidue = min(residue, minResidue)
    return minResidue

### Repeated Random with prepartitions ###
def rrPrePart(A):
    minResidue = maxint
    for _ in xrange(NUM_TRIALS):
        P = genPrepartition()
        APartitioned = [0] * INPUT_LEN
        for i in xrange(INPUT_LEN):
            APartitioned[P[i]] += A[i]
        residue = kk(APartitioned)
        minResidue = min(residue, minResidue)
    return minResidue

def main():
    A = []
    if len(argv) < 2:
        ## print "Usage: python ./kk.py inputfile"
        ## exit(1)
        A = getArray()
    else:
        A = getArray(argv[1])
    print kk(A[:])
    print rrSeq(A[:])
    print rrPrePart(A[:])
    
main()



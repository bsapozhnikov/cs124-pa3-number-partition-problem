from sys import argv, exit, maxint
from time import time
import random, math

INPUT_LEN = 100
MAX_VAL = 10 ** 12
NUM_ITERS = 25000
NUM_TRIALS = 100

####################
###   HELPERS    ###
####################

### getArray(filename)
###   reads array from file named `filename` and returns it
### Invariant: `filename` is a list of INPUT_LEN integers, one per line
def getArray(filename):
    inputfile = open(filename, 'r')
    return [int(inputfile.readline()) for _ in xrange(INPUT_LEN)]

### genRandArray()
###   generates and returns random array of INPUT_LEN values,
###   each between 0 and MAX_VAL, inclusive
def genRandArray():
    return [random.randint(0, MAX_VAL) for _ in xrange(INPUT_LEN)]
    
### genSolutionSeq()
###   generate and return a random solution,
###   represented as a list of +1s and -1s
def genSolutionSeq():
    return [random.choice([-1, 1]) for _ in xrange(INPUT_LEN)]

### genPrepartition()
###   generate and return a random prepartition,
###   represented as a list of random group ids
def genPrepartition():
    return [random.randint(0, INPUT_LEN - 1) for _ in xrange(INPUT_LEN)]

### genSeqNeighbor(S)
###   generate and return a random neighbor for a solution sequence,
###   where moving from S to a neighbor is accomplished by swapping
###   either one or two elements of S
### Invariant: S is a valid solution sequence
def genSeqNeighbor(S):
    sample = random.sample(xrange(INPUT_LEN), 2)
    S[sample[0]] *= -1
    if (random.randint(0, 1)):
        S[sample[1]] *= -1
    return S

### genPrePartNeighbor(P)
###   generate and return a random neighbor for a prepartition,
###   where moving from P to a neighbor is accomplished by changing
###   which partition on element lies in
### Invariant: P is a valid prepartition
def genPrePartNeighbor(P):
    sample = random.sample(xrange(INPUT_LEN), 2)
    while (P[sample[0]] == sample[1]):
        sample = random.sample(xrange(INPUT_LEN), 2)
    P[sample[0]] = sample[1]
    return P
    
### binsert()
###   insert x into A in sorted position, using binary search
### Invariant: A is sorted
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

### prePartition(A, P)
###   partition a list given a prepartition
### Invariant: len(A) == INPUT_LEN; P is a valid prepartition
def prePartition(A, P):
    APartitioned = [0] * INPUT_LEN
    for i in xrange(INPUT_LEN):
        APartitioned[P[i]] += A[i]
    return APartitioned

### getResidueSeq(A, S)
###   return residue given array A and sequence S
### Invariants: len(A) == INPUT_LEN; A is a valid solution sequence
def getResidueSeq(A, S):
    return abs(sum(A[i] * S[i] for i in xrange(INPUT_LEN)))

### getResiduePP(A, P)
###   return residue given array A and partition P
### Invariants: len(A) == INPUT_LEN; P is a valid prepartition
def getResiduePP(A, P):
    return kk(prePartition(A,P))

### saCooling(i)
###   cooling schedule function for simulated annealing ###
def saCooling(i):
    return (10**8) * (0.8**(i // 300))

####################
###  EXPERIMENT  ###
####################

def timing(f):
    def wrap(*args):
        start = time()
        res = f(*args)
        end = time()
        return (res, end - start)
    return wrap

def experiment(f):
    def wrap(_A):
        resSum = timeSum = 0
        for _ in xrange(NUM_TRIALS):
            (res, time) = timing(f)(genRandArray())
            resSum += res
            timeSum += time
        return (resSum / NUM_TRIALS, timeSum / NUM_TRIALS)
    return wrap

####################
###  ALGORITHMS  ###
####################

### Karmarkar-Karp
def kk(A):
    A.sort()
    for _ in xrange(len(A)-1):
        m1 = A.pop()
        m2 = A.pop()
        binsert(A, abs(m1 - m2))
    return A[0]

### Repeated Random with solution sequences
@experiment
def rrSeq(A):
    minResidue = maxint
    for _ in xrange(NUM_ITERS):
        S = genSolutionSeq()
        residue = getResidueSeq(A, S)
        minResidue = min(residue, minResidue)
    return minResidue

### Repeated Random with prepartitions
@experiment
def rrPrePart(A):
    minResidue = maxint
    for _ in xrange(NUM_ITERS):
        P = genPrepartition()
        residue = getResiduePP(A, P)
        minResidue = min(residue, minResidue)
    return minResidue

### Hill Climbing with solution sequences
@experiment
def hcSeq(A):
    S = genSolutionSeq()
    minResidue = getResidueSeq(A, S)
    for _ in xrange(NUM_ITERS):
        SNeighbor = genSeqNeighbor(S[:])
        residue = getResidueSeq(A, SNeighbor)
        if residue < minResidue:
            S = SNeighbor
            minResidue = residue
    return minResidue

### Hill Climbing with prepartitions
@experiment
def hcPrePart(A):
    P = genPrepartition()
    minResidue = getResiduePP(A, P)
    for _ in xrange(NUM_ITERS):
        PNeighbor = genPrePartNeighbor(P[:])
        residue = getResiduePP(A, PNeighbor)
        if residue < minResidue:
            P = PNeighbor
            minResidue = residue
    return minResidue

### Simulated Annealing with solution sequences
@experiment
def saSeq(A):
    S = genSolutionSeq()
    minResidue = maxint
    for i in xrange(NUM_ITERS):
        SNeighbor = genSeqNeighbor(S[:])
        residueS = getResidueSeq(A, S)
        residueSNeighbor = getResidueSeq(A, SNeighbor)
        if residueSNeighbor < residueS:
            S = SNeighbor
            residueS = residueSNeighbor
        else:
            moveProb = math.exp(-1.0 * (residueSNeighbor - residueS) / saCooling(i))
            if random.uniform(0, 1) <= moveProb:
                S = SNeighbor
                residueS = residueSNeighbor
        minResidue = min(residueS, minResidue)
    return minResidue

### Simulated Annealing with prepartitions
@experiment
def saPrePart(A):
    P = genPrepartition()
    minResidue = maxint
    for i in xrange(NUM_ITERS):
        PNeighbor = genPrePartNeighbor(P[:])
        residueP = getResiduePP(A, P)
        residuePNeighbor = getResiduePP(A, PNeighbor)
        if residuePNeighbor < residueP:
            P = PNeighbor
            residueP = residuePNeighbor
        else:
            moveProb = math.exp(-1.0 * (residuePNeighbor - residueP) / saCooling(i))
            if random.uniform(0, 1) <= moveProb:
                P = PNeighbor
                residueP = residuePNeighbor
        minResidue = min(residueP, minResidue)
    return minResidue

####################
###     MAIN     ###
####################

def main():
    A = []
    if len(argv) < 2:
        A = genRandArray()
    else:
        A = getArray(argv[1])
        print kk(A[:])
        return
    ## cannot decorate KK since it's used by other functions
    print "KK:  " + str(experiment(kk)(A[:]))
    print "RRS: " + str(rrSeq(A[:]))
    print "RRP: " + str(rrPrePart(A[:]))
    print "HCS: " + str(hcSeq(A[:]))
    print "HCP: " + str(hcPrePart(A[:]))
    print "SAS: " + str(saSeq(A[:]))
    print "SAP: " + str(saPrePart(A[:]))
    
main()



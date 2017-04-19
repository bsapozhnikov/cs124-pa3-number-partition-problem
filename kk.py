from sys import argv, exit, maxint
import random, math

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

### Partition a list given a prepartition ###
def prePartition(A, P):
    APartitioned = [0] * INPUT_LEN
    for i in xrange(INPUT_LEN):
        APartitioned[P[i]] += A[i]
    return APartitioned
    

### Generate and return a random       ###
###   neighbor for a solution sequence ###
def genSeqNeighbor(S):
    sample = random.sample(xrange(INPUT_LEN), 2)
    S[sample[0]] *= -1
    if (random.randint(0, 1)):
        S[sample[1]] *= -1
    return S

### Generate and return a random  ###
###   neighbor for a prepartition ###
def genPrePartNeighbor(P):
    sample = random.sample(xrange(INPUT_LEN), 2)
    while (P[sample[0]] == sample[1]):
        sample = random.sample(xrange(INPUT_LEN), 2)
    P[sample[0]] = sample[1]
    return P
    
### Return residue given array A and sequence S ###
###   A[i] is in partition "1" iff S[i] == 1    ###
###   else A[i] is in partition "-1"            ###
### Invariants:                                 ###
###   S[i] == 1 or S[i] == -1 for all i         ###
###   len(A) == len(S) == INPUT_LEN             ###
def getResidueSeq(A,S):
    return abs(sum(A[i] * S[i] for i in xrange(INPUT_LEN)))
    
### Return residue given array A and partition P ###
###   A[i] is in partition group P[i]            ###
### Invariants:                                  ###
###   len(A) == len(P) == INPUT_LEN              ###
###   0 <= P[i] <= INPUT_LEN for all i           ###
def getResiduePP(A,P):
    return kk(prePartition(A,P))

### Repeated Random with solution sequences ###
def rrSeq(A):
    minResidue = maxint
    for _ in xrange(NUM_TRIALS):
        S = genSolutionSeq()
        residue = getResidueSeq(A, S)
        minResidue = min(residue, minResidue)
    return minResidue

### Repeated Random with prepartitions ###
def rrPrePart(A):
    minResidue = maxint
    for _ in xrange(NUM_TRIALS):
        P = genPrepartition()
        residue = getResiduePP(A, P)
        minResidue = min(residue, minResidue)
    return minResidue

### Hill Climbing with solution sequences ###
def hcSeq(A):
    S = genSolutionSeq()
    minResidue = getResidueSeq(A, S)
    for _ in xrange(NUM_TRIALS):
        SNeighbor = genSeqNeighbor(S[:])
        residue = getResidueSeq(A, SNeighbor)
        if residue < minResidue:
            S = SNeighbor
            minResidue = residue
    return minResidue

### Hill Climbing with prepartitions ###
def hcPrePart(A):
    P = genPrepartition()
    minResidue = getResiduePP(A, P)
    for _ in xrange(NUM_TRIALS):
        PNeighbor = genPrePartNeighbor(P[:])
        residue = getResiduePP(A, PNeighbor)
        if residue < minResidue:
            P = PNeighbor
            minResidue = residue
    return minResidue

### Cooling schedule function for simulated annealing ###
def saCooling(i):
    return (10**8) * (0.8**(i // 300))

### Simulated Annealing with solution sequences ###
def saSeq(A):
    S = genSolutionSeq()
    minResidue = getResidueSeq(A, S)
    for i in xrange(NUM_TRIALS):
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

### Simulated Annealing with prepartitions ###
def saPrePart(A):
    P = genPrepartition()
    minResidue = getResiduePP(A, P)
    for i in xrange(NUM_TRIALS):
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
    print hcSeq(A[:])
    print hcPrePart(A[:])
    print saSeq(A[:])
    print saPrePart(A[:])
    
main()



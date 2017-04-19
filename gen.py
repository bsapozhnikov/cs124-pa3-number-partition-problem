from sys import argv, exit
from random import randint

INPUT_LEN = 100

if len(argv) < 2:
    print "Usage: python ./gen.py outputfile"
    exit(1)

file = open(argv[1], "w")

for _ in xrange(INPUT_LEN):
    file.write(str(randint(0, 10 ** 12)) + '\n')

#!/usr/bin/python

import sys
import math

def is_square(n):
    sq = int(math.sqrt(n))
    return n == sq * sq

def doublesquares(number):
    n = 0
    count = 0
    max_nsq = number + 1

    while True:
        #print "  # %s" % n
        nsq = n * n

        if nsq >= max_nsq:
            break

        if is_square(number - nsq):
            #print "    * %s %s" % (nsq, number - nsq)
            count += 1
            max_nsq = number - nsq

        n += 1
    
    return count
            


def main(argv):
    for filename in argv[1:]:
        with open(filename) as f:
            count = int(f.readline())
            for _ in xrange(count):
                line = f.readline()
                print doublesquares(int(line))

if __name__ == '__main__':
    main(sys.argv)

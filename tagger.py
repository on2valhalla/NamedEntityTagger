#! /usr/bin/python

__author__="Jason Mann <jcm2207@cs.columbia.edu>"
__date__ ="$Sep 20, 2013"

import sys
from collections import defaultdict
import math

import count_freqs
from count_freqs import Hmm

"""
Read in counts file and tag development data
"""

def usage():
    print """
    python tagger.py [counts_file] [test_file] > [output_file]
        Read in counts file and test data and outputs tagged data
    """

if __name__ == "__main__":

    elif len(sys.argv)!=3: # Expect exactly two arguments: the counts file and test data
        usage()
        sys.exit(2)

    try:
        countfile = file(sys.argv[1],"r")
        testfile = file(sys.argv[2], 'r')
        taggedfile = file(sys.argv[2] + '.tagged', 'w')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Collect counts
    counter.read_counts(countfile)

    # Replace the rare words in the corpus and counts
    if replace_rare:
        countfile.seek(0)
        counter.replace_rare(countfile, testfile)

    # Write the counts
    counter.write_counts(sys.stdout)

    # Close files
    countfile.close()
    testfile.close()

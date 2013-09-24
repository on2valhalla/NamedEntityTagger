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


class EmissionProbabilityTagger(object):
    """
    Stores counts for n-grams and emissions. 
    """

    def __init__(self, hmm):
        self.hmm = hmm
        self.seen_tags = defaultdict(str)

    def tag_data(self, testfile, tagfile_out):
        for line in testfile:
            word = line.strip()
            if word == '':
                tagfile_out.write('\n')
                continue
            max_prob = 0
            max_tag = None
            for tag in self.hmm.all_states:
                em_prob = self.hmm.emission_probability(word, tag)
                if max_prob < em_prob:
                    max_prob = em_prob
                    max_tag = tag


            if max_prob > 0:
                max_prob = math.log(max_prob, 2)
            else:
                max_prob = 0

            if max_tag is not None:
                self.seen_tags[word] = max_tag + ' ' + str(max_prob)
            else:
                sys.stderr.write(word + ' NOT_FOUND\n')
                self.seen_tags[word] = 'NOT_FOUND'

            sys.stderr.write(word + ' ' + self.seen_tags[word] + '\n')
            tagfile_out.write(word + ' ' + self.seen_tags[word] + '\n')




def usage():
    print """
    python tagger.py [counts_file] [test_file] > [output_file]
        Read in counts file and test data and outputs tagged data
    """

if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly two arguments: the counts file and test data
        usage()
        sys.exit(2)

    try:
        countfile = file(sys.argv[1],"r")
        testfile = file(sys.argv[2], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Read in counts
    counter.read_counts(countfile)

    # Tag the data
    tagger = EmissionProbabilityTagger(counter)
    tagger.tag_data(testfile, sys.stdout)

    # Close files
    countfile.close()
    testfile.close()

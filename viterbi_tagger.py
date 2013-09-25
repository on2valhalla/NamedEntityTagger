#! /usr/bin/python

__author__="Jason Mann <jcm2207@cs.columbia.edu>"
__date__ ="$Sep 20, 2013"

import sys
from collections import defaultdict
import math

from count_freqs import Hmm, sentence_iterator, simple_conll_corpus_iterator

"""
Read in counts file and tag development data
"""

class ViterbiEntityTagger(object):
    """
    Entity tagger using HMM trained on maximum likelyhood trigram probabilities
    """

    def __init__(self, hmm):
        self.hmm = hmm
        # trigram length to condition on
        self.ngram_len = 3

    def tag_data(self, testfile, tagfile_out):

        all_tags = self.hmm.all_states

        sent_iterator = sentence_iterator(simple_conll_corpus_iterator(testfile))

        for sent in sent_iterator:
            # initialize variables and dynamic programming tables
            n = len(sent)
            pi = defaultdict(int)
            bp = defaultdict(str)

            pi[(-1,'*','*')] = 1

            for i in range(n):
                for v in all_tags:
                    for u in all_tags if i > 0 else ['*']:
                        max_prob = 0
                        max_tag = None
                        for w in all_tags if i > 1 else ['*']:
                            prob = (pi[(i-1, w, u)] * self.hmm.ml_prob(v, (w, u))
                                        * self.hmm.emission_prob(sent[i][0], v))
                            # sys.stderr.write(str((i-1, w, u)) + '\t' + str(self.hmm.ml_prob(v, (w, u)))
                            #      + '\t' + str(self.hmm.emission_prob(sent[i][0], v)) + '\t' + str(prob) + '\n')
                            if max_prob < prob:
                                max_prob = prob
                                max_tag = w

                        pi[(i, u, v)] = max_prob
                        bp[(i, u, v)] = max_tag

            max_sent_prob = 0
            final_tags = [None]*n
            for u in all_tags:
                for v in all_tags:
                    prob = pi[(n-1, u, v)] * self.hmm.ml_prob('STOP', (u, v))
                    if max_sent_prob < prob:
                        max_sent_prob = prob
                        final_tags[n-2] = u
                        final_tags[n-1] = v

            for i in range(n-3, -1, -1):
                # sys.stderr.write(str(i) + '\n')
                final_tags[i] = bp[(i+2, final_tags[i+1], final_tags[i+2])]

            # sys.stderr.write(str(final_tags))

            for i in range(n-3):
                # sys.stderr.write(str(i) + '\n')
                word = sent[i][0]
                tag = final_tags[i]
                log_prob = math.log(pi[(i, final_tags[i+1], final_tags[i+2])], 2)
                tagfile_out.write('%s %s %f\n' % (word, tag, log_prob))

            tagfile_out.write('%s %s %f\n' % (sent[n-2][0], final_tags[n-2], math.log(max_sent_prob, 2)))
            tagfile_out.write('%s %s %f\n' % (sent[n-1][0], final_tags[n-1], math.log(max_sent_prob, 2)))

            tagfile_out.write('\n')










            # word = line.strip()
            # if word == '':
            #     tagfile_out.write('\n')
            #     continue
            # max_prob = 0
            # max_tag = None
            # for tag in self.hmm.all_states:
            #     prob = self.hmm.max_likelyhood_trigram(ngram)
            #     if max_prob < prob:
            #         max_prob = prob
            #         max_tag = tag

            # if max_prob > 0:
            #     max_prob = math.log(max_prob, 2)
            # else:
            #     max_prob = 0

            # if max_tag is not None:
            #     self.seen_tags[word] = max_tag + ' ' + str(max_prob)
            # else:
            #     sys.stderr.write(word + ' NOT_FOUND\n')
            #     self.seen_tags[word] = 'NOT_FOUND'

            # tagfile_out.write(word + ' ' + self.seen_tags[word] + '\n')


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
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % sys.argv[1])
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Read in counts
    counter.read_counts(countfile)

    # Tag the data
    tagger = ViterbiEntityTagger(counter)
    tagger.tag_data(testfile, sys.stdout)

    # Close files
    countfile.close()
    testfile.close()

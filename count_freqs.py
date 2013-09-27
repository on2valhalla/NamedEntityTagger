#! /usr/bin/python

__author__="Daniel Bauer <bauer@cs.columbia.edu> and Jason Mann <jcm2207@columbia.edu>"
__date__ ="$Sep 12, 2011"

import sys
from collections import defaultdict
import math
import re

"""
Count n-gram frequencies in a CoNLL NER data file and write counts to
stdout. 
"""

def simple_conll_corpus_iterator(corpus_file):
    """
    Get an iterator object over the corpus file. The elements of the
    iterator contain (word, ne_tag) tuples. Blank lines, indicating
    sentence boundaries return (None, None).
    """
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            # Extract information from line.
            # Each line has the format
            # word pos_tag phrase_tag ne_tag
            fields = line.split(" ")
            ne_tag = fields[-1] if len(fields) > 1 else None
            #phrase_tag = fields[-2] #Unused
            #pos_tag = fields[-3] #Unused
            word = " ".join(fields[:-1]) if len(fields) > 1 else fields[-1]
            yield (word, ne_tag)
        else: # Empty line
            yield (None, None)                
        l = corpus_file.readline()

def sentence_iterator(corpus_iterator):
    """
    Return an iterator object that yields one sentence at a time.
    Sentences are represented as lists of (word, ne_tag) tuples.
    """
    current_sentence = [] #Buffer for the current sentence
    for l in corpus_iterator:
            if l==(None, None):
                if current_sentence:  #Reached the end of a sentence
                    yield current_sentence
                    current_sentence = [] #Reset buffer
                else: # Got empty input stream
                    sys.stderr.write("WARNING: Got empty input file/stream.\n")
                    raise StopIteration
            else:
                current_sentence.append(l) #Add token to the buffer

    if current_sentence: # If the last line was blank, we're done
        yield current_sentence  #Otherwise when there is no more token
                                # in the stream return the last sentence.

def get_ngrams(sent_iterator, n):
    """
    Get a generator that returns n-grams over the entire corpus,
    respecting sentence boundaries and inserting boundary tokens.
    Sent_iterator is a generator object whose elements are lists
    of tokens.
    """
    for sent in sent_iterator:
         #Add boundary symbols to the sentence
         w_boundary = (n-1) * [(None, "*")]
         w_boundary.extend(sent)
         w_boundary.append((None, "STOP"))
         #Then extract n-grams
         ngrams = (tuple(w_boundary[i:i+n]) for i in xrange(len(w_boundary)-n+1))
         for n_gram in ngrams: #Return one n-gram at a time
            yield n_gram        


ALLCAPS = '_ALLCAPS_'
ALLNUM = '_ALLNUM_'
CAPPERIOD = '_CAPPERIOD_'
INITCAP = '_INITCAP_'
# FIRSTWORD = '_FIRSTWORD_'
LOWERCASE = '_LOWERCASE_'
# NUM2D = '_NUM2D_'
NUM4D = '_NUM4D_'
NUMALPHA = '_NUMALPHA_'
NUMCOMMA = '_NUMCOMMA_'
NUMDASH = '_NUMDASH_'
NUMOTHER = '_NUMOTHER_'
NUMPERIOD = '_NUMPERIOD_'
NUMSLASH = '_NUMSLASH_'
RARE = '_RARE_'

all_rare_types = [ALLCAPS,
                  ALLNUM,
                  CAPPERIOD,
                  INITCAP,
                  # FIRSTWORD,
                  LOWERCASE,
                  # NUM2D,
                  NUM4D,
                  NUMALPHA,
                  NUMCOMMA,
                  NUMDASH,
                  NUMOTHER,
                  NUMPERIOD,
                  NUMSLASH,
                  RARE]

RE_DIGIT = re.compile(r'\d')
RE_ALPHA = re.compile(r'[a-zA-Z]')
RE_DASH = re.compile(r'[-]')
RE_SLASH = re.compile(r'[/\\]')
RE_COMMA = re.compile(r',')
RE_PERIOD = re.compile(r'[.]')
RE_CAP = re.compile(r'[A-Z]')

RE_ALLDIGIT = re.compile(r'\A\d*\Z')
RE_ALLCAPS = re.compile(r'\A[A-Z]*\Z')
RE_INITIALS = re.compile(r'\A([A-Z][.])*\Z')
RE_INITCAP = re.compile(r'\A[A-Z][^A-Z]*\Z')
RE_LOWER = re.compile(r'\A[a-z]*\Z')



class Hmm(object):
    """
    Stores counts for n-grams and emissions. 
    """

    def __init__(self, n=3):
        assert n>=2, "Expecting n>=2."
        self.n = n
        self.low_freq = 5
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.word_counts = defaultdict(int)
        self.all_states = set()
        self.rare_word_symbols = defaultdict(str)

    def train(self, corpus_file):
        """
        Count n-gram frequencies and emission probabilities from a corpus file.
        """
        ngram_iterator = \
            get_ngrams(sentence_iterator(simple_conll_corpus_iterator(corpus_file)), self.n)

        for ngram in ngram_iterator:
            #Sanity check: n-gram we get from the corpus stream needs to have the right length
            assert len(ngram) == self.n, "ngram in stream is %i, expected %i" % (len(ngram, self.n))

            tagsonly = tuple([ne_tag for word, ne_tag in ngram]) #retrieve only the tags            
            for i in xrange(2, self.n+1): #Count NE-tag 2-grams..n-grams
                self.ngram_counts[i-1][tagsonly[-i:]] += 1
            
            if ngram[-1][0] is not None: # If this is not the last word in a sentence
                self.ngram_counts[0][tagsonly[-1:]] += 1 # count 1-gram
                self.emission_counts[ngram[-1]] += 1 # and emission frequencies
                self.word_counts[ngram[-1][0]] += 1 # and word counts
                self.all_states.add(ngram[-1][1])  # add tag to a set recording all seen

            # Need to count a single n-1-gram of sentence start symbols per sentence
            if ngram[-2][0] is None: # this is the first n-gram in a sentence
                self.ngram_counts[self.n - 2][tuple((self.n - 1) * ["*"])] += 1

    def write_counts(self, output, printngrams=[1,2,3]):
        """
        Writes counts to the output file object.
        Format:
            [count] WORDTAG [tag] [word]
            [count] [n]-GRAM [tag] ([tag]) ([tag])
            [count] WORDCOUNT [word]
        """
        # First write counts for emissions
        for word, ne_tag in self.emission_counts:            
            output.write("%i WORDTAG %s %s\n" % (self.emission_counts[(word, ne_tag)], ne_tag, word))


        # Then write counts for all ngrams
        for n in printngrams:            
            for ngram in self.ngram_counts[n-1]:
                ngramstr = " ".join(ngram)
                output.write("%i %i-GRAM %s\n" %(self.ngram_counts[n-1][ngram], n, ngramstr))

        # And counts for all words  
        for word in self.word_counts:
            output.write("%i WORDCOUNT %s\n" %(self.word_counts[word], word))

    def read_counts(self, countsfile):
        """
        Read in counts of a corpus from a file specified by countsfile
        and store them in objects
        """

        self.n = 3
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.all_states = set()

        for line in countsfile:
            parts = line.strip().split(" ")
            count = float(parts[0])
            if parts[1] == "WORDTAG":
                ne_tag = parts[2]
                word = parts[3]
                self.emission_counts[(word, ne_tag)] = count
                self.all_states.add(ne_tag)
            elif parts[1].endswith("GRAM"):
                n = int(parts[1].replace("-GRAM",""))
                ngram = tuple(parts[2:])
                self.ngram_counts[n-1][ngram] = count
            elif parts[1] == "WORDCOUNT":
                # Keep track of word counts for _RARE_ labelling automation
                word = parts[-1]
                self.word_counts[word] = count


    ########################################################
    #########  Functions by Jason Mann #####################
    ########################################################
    
    def rare_symbol(self, word = None, firstword = False):
        """
        Assign symbols to rare words based on simple lexical categories, or just _RARE_
        """
        symbol = RARE

        if word in self.rare_word_symbols:
            # for speed, due to multiple lookups for each word
            symbol = self.rare_word_symbols[word]
        elif word is not None:
            if RE_DIGIT.search(word):
                # if RE_ALLDIGIT.match(word):
                #     # if len(word) == 2:
                #     #     symbol = NUM2D
                #     if len(word) == 4:
                #         symbol = NUM4D
                #     else:
                #         symbol = ALLNUM
                # elif RE_ALPHA.search(word):
                #     symbol = NUMALPHA
                # elif RE_DASH.search(word):
                #     symbol = NUMDASH
                # elif RE_SLASH.search(word):
                #     symbol = NUMSLASH
                # elif RE_COMMA.search(word):
                #     symbol = NUMCOMMA
                # elif RE_PERIOD.search(word):
                #     symbol = NUMPERIOD
                # else:
                symbol = NUMOTHER
            else:
                if RE_LOWER.match(word):
                    symbol = LOWERCASE
                elif RE_INITIALS.match(word):
                    symbol = CAPPERIOD
                # elif firstword:
                #     symbol = FIRSTWORD
                elif RE_INITCAP.match(word):
                    symbol = INITCAP
                elif RE_ALLCAPS.match(word):
                    init_cap = word.capitalize()
                    lower = word.lower()
                    # Have to check if they are in the dict first, so that we dont
                    # change the size of the dict while a higher level loop is running
                    if init_cap in self.word_counts and lower in self.word_counts:
                        if self.word_counts[init_cap] >= self.word_counts[lower]:
                            symbol = init_cap
                        else:
                            symbol = lower
                    elif init_cap in self.word_counts:
                        symbol = init_cap
                    elif lower in self.word_counts:
                        symbol = lower
                    else:
                        symbol = ALLCAPS
            # sys.stderr.write('%s %s\n' % (word, symbol))

        self.rare_word_symbols[word] = symbol
        return symbol

    def replace_rare(self, corpusfile, rarecorpusfile):
        for rare_type in all_rare_types:
            self.word_counts[rare_type] = 0
            for ne_tag in self.all_states:
                self.emission_counts[(rare_type, ne_tag)] = 0

        rare_words = set()
        for word in self.word_counts:
            count = self.word_counts[word]
            if count < self.low_freq:
                rare_type = self.rare_symbol(word)

                # delete the count for this word and add it to the rare count
                self.word_counts[rare_type] += count
                rare_words.add(word)

                # do the same for each tag's emission counts
                for ne_tag in self.all_states:
                    if (word, ne_tag) in self.emission_counts:
                        self.emission_counts[(rare_type, ne_tag)] += self.emission_counts[(word, ne_tag)]
                        del self.emission_counts[(word, ne_tag)]

        # remove rare counts
        for word in rare_words:
            del self.word_counts[word]

        sys.stderr.write(str(sorted({k:v for k,v in self.word_counts.items() if k.startswith('_') or v < 5}.items()))+'\n\n')

        # write to the new corpus file
        sent_iterator = sentence_iterator(simple_conll_corpus_iterator(corpusfile))
        for sent in sent_iterator:
            firstword = True
            for word, tag in sent:
                if word in rare_words:
                    # Find the correct bucket for the rare word seen and replace with
                    # a symbol representing it.
                    word = self.rare_symbol(word, firstword)

                if firstword and word is not "\"":
                    firstword = False
                    
                rarecorpusfile.write('%s %s\n' % (word, tag))
            rarecorpusfile.write('\n')

    def emission_prob(self, word, tag):
        if (word, tag) in self.emission_counts:  # pair has a valid emission count
            return self.emission_counts[(word, tag)] / self.ngram_counts[0][(tag,)]
        elif word in self.word_counts:  # word exists with another tag, set this prob as 0
            return 0
        elif tag in self.all_states: # word not found in set, treat as rare
            return self.emission_counts[(self.rare_symbol(word), tag)] / self.ngram_counts[0][(tag,)]
        else:  # tag was not found in set
            sys.stderr.write("Faulty arguments for emission probability")
            return -1

    def ml_prob(self, tag, bigram):
        """
        Ngram is a tuple representing a trigram of tags
        """
        trigram = bigram + (tag,)
        if bigram in self.ngram_counts[1] and trigram in self.ngram_counts[2]:
            # both the trigram and bigram have valid counts
            return self.ngram_counts[2][trigram] / self.ngram_counts[1][bigram]
        elif tag in self.all_states.union(['STOP']) and bigram[0] in self.all_states.union(['*']) \
            and bigram[1] in self.all_states.union(['*']):
            return 0
        else:
            sys.stderr.write("Faulty arguments for trigram max likelyhood probability")
            return -1



def usage():
    print """
    python count_freqs.py [input_file] (rare) > [output_file]
        Read in a named entity tagged training input file and produce counts.
    """

if __name__ == "__main__":

    replace_rare = False
    if len(sys.argv) == 3 and sys.argv[2] == 'rare':  # second argument is a signal to replace rare words
        replace_rare = True
    elif len(sys.argv)!=2: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        input = file(sys.argv[1],"r")
        rarecorpusfile = file(sys.argv[1] + '.rare', 'w')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % sys.argv[1])
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Collect counts
    counter.train(input)

    # Replace the rare words in the corpus and counts
    if replace_rare:
        input.seek(0)
        counter.replace_rare(input, rarecorpusfile)

    # Write the counts
    counter.write_counts(sys.stdout)

    # Close files
    input.close()
    rarecorpusfile.close()

import eval_ne_tagger
import count_freqs
import viterbi_tagger


def usage():
    sys.stderr.write("""
    Usage: python eval_ne_tagger.py [key_file] [prediction_file]
        Evaluate the NE-tagger output in prediction_file against
        the gold standard in key_file. Output accuracy, precision,
        recall and F1-Score for each NE tag type.\n""")

if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly two arguments: the corpus file and test data
        usage()
        sys.exit(2)

    try:
        corpusfile = open(sys.argv[1],'r')
        rarecorpusfile = open(sys.argv[1] + '.rare', 'w')
        countfile = open(sys.argv[1] + '.counts','w')
        testfile = open(sys.argv[2], 'r')
        taggedfile = open(sys.argv[2] + '.tagged','w')
    except IOError:
        sys.stderr.write("ERROR: Cannot open one of the files %s.\n")
        sys.exit(1)


    # Initialize the objects
    counter = count_freqs.Hmm(3)

    # Tag the data
    tagger = viterbi_tagger.ViterbiEntityTagger(counter)
    tagger.tag_data(testfile, sys.stdout)
    
    for i to range(len(all_rare_types)):
        
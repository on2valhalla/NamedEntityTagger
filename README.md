Jason Carlisle Mann
jcm2207@columbia.edu

Question 4
==========

1: How to run
-------------
-To collect counts, with _RARE_ replacement:
	$ python count_freqs.py ner_train.dat rare > ner.counts

-To run the tagger on the test data:
	$ python emission_tagger.py ner.counts ner_dev.dat > ner_dev.tagged

-Evaluation was run using:
	$ eval_ne_tagger.py ner_dev.key ner_dev.tagged


Results
-------
Found 14043 NEs. Expected 5931 NEs; Correct: 3117.

	 precision 	recall 		F1-Score
Total:	 0.221961	0.525544	0.312106
PER:	 0.435451	0.231230	0.302061
ORG:	 0.475936	0.399103	0.434146
LOC:	 0.147750	0.870229	0.252612
MISC:	 0.491689	0.610206	0.544574



Question 5
==========
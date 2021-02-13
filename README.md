
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


Implementation Notes
--------------------
I kept track of word counts to assist with assigning zero emission probabilities.



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


Results
-------
Found 4704 NEs. Expected 5931 NEs; Correct: 3647.

	 precision 	recall 		F1-Score
Total:	 0.775298	0.614905	0.685849
PER:	 0.762535	0.595756	0.668907
ORG:	 0.611855	0.478326	0.536913
LOC:	 0.876458	0.696292	0.776056
MISC:	 0.830065	0.689468	0.753262



Question 6
==========

Numbers only
------------
Found 5022 NEs. Expected 5931 NEs; Correct: 3721.

	 precision 	recall 		F1-Score
Total:	 0.740940	0.627382	0.679449
PER:	 0.683589	0.630033	0.655719
ORG:	 0.613296	0.489537	0.544472
LOC:	 0.851135	0.695202	0.765306
MISC:	 0.830709	0.687296	0.752228

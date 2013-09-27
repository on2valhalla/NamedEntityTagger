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

All buckets without first word
------------------------------

[('_ALLCAPS_', 758), ('_ALLNUM_', 565), ('_CAPPERIOD_', 63), ('_INITCAP_', 10532), ('_LOWERCASE_', 11167), ('_NUM4D_', 321), ('_NUMALPHA_', 660), ('_NUMCOMMA_', 547), ('_NUMOTHER_', 94), ('_NUMPERIOD_', 1927), ('_NUMSLASH_', 86), ('_RARE_', 1386)]

Found 5890 NEs. Expected 5931 NEs; Correct: 4373.

	 precision 	recall 		F1-Score
Total:	 0.742445	0.737312	0.739870
PER:	 0.810112	0.784548	0.797125
ORG:	 0.534994	0.674141	0.596561
LOC:	 0.850336	0.758997	0.802074
MISC:	 0.809403	0.691640	0.745902


No Number Specification
-----------------------

[('_ALLCAPS_', 758), ('_CAPPERIOD_', 63), ('_INITCAP_', 10532), ('_LOWERCASE_', 11167), ('_NUMOTHER_', 4897), ('_RARE_', 1386)]






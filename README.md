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

'_ALLCAPS_': 		2204
'_ALLNUM_':			565
'_CAPPERIOD_':		63
'_INITCAP_':		10514
'_LOWERCASE_':		11196
'_NUM4D_':			321
'_NUMALPHA_':		660
'_NUMCOMMA_':		547
'_NUMOTHER_':		94
'_NUMPERIOD_':		1927
'_NUMSLASH_':		86
'_RARE_':		 	1386

Found 4314 NEs. Expected 5931 NEs; Correct: 3525.

	 precision 	recall 		F1-Score
Total:	 0.817107	0.594335	0.688141
PER:	 0.854202	0.541893	0.663116
ORG:	 0.669501	0.470852	0.552874
LOC:	 0.893676	0.701200	0.785823
MISC:	 0.798177	0.665581	0.725873



'_ALLCAPS_':		 2204
'_ALLNUM_':			 565
'_CAPPERIOD_':		 18
'_INITCAP_':		 10588
'_LOWERCASE_':		 11196
'_NUM4D_':			 321
'_NUMALPHA_':		 3519
'_RARE_':			 1829

Found 4266 NEs. Expected 5931 NEs; Correct: 3508.

	 precision 	recall 		F1-Score
Total:	 0.822316	0.591469	0.688046
PER:	 0.862377	0.525027	0.652689
ORG:	 0.674840	0.473094	0.556239
LOC:	 0.892436	0.701200	0.785344
MISC:	 0.812500	0.677524	0.738899

'_ALLCAPS_':		2204
'_ALLNUM_':			565
'_CAPPERIOD_':		18
'_INITCAP_':		10514
'_LOWERCASE_':		11196
'_NUM4D_':			321
'_NUMALPHA_':		3991
'_RARE_':			1431

Found 4418 NEs. Expected 5931 NEs; Correct: 3506.

	 precision 	recall 		F1-Score
Total:	 0.793572	0.591131	0.677553
PER:	 0.851282	0.541893	0.662234
ORG:	 0.612840	0.470852	0.532544
LOC:	 0.884298	0.700109	0.781497
MISC:	 0.776042	0.647123	0.705743


'_INITCAP_', 		10552
'_LOWERCASE_':		11196
'_NUMOTHER_':		4897
'_RARE_':			3615

Found 6925 NEs. Expected 5931 NEs; Correct: 3771.

	 precision 	recall 		F1-Score
Total:	 0.544549	0.635812	0.586652
PER:	 0.487101	0.688248	0.570462
ORG:	 0.423611	0.592676	0.494081
LOC:	 0.701991	0.653762	0.677019
MISC:	 0.687166	0.558089	0.615938
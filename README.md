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

For this question, I started out with all of the different buckets that were presented in the class notes: 
	_ALLCAPS_, _ALLNUM_, _CAPPERIOD_, _INITCAP_, _LOWERCASE_, _NUM4D_, _NUMALPHA_, _NUMCOMMA_, _NUMOTHER_, _NUMPERIOD_, _NUMSLASH_, _RARE_

Some of the groupings from class were omitted, while they were not expressed in the training data. These initial groupings caused a 5 point increase in the overall F1 score. 

My next trials were based on mostly linguistic reasoning, and an attempt to distinguish between important rare categories for named entities.

I started by grouping all the number types together, while numbers in the training data are not likely to be named entities, which caused a minimal improvement. Another minimal improvement was to try and find the correct capitalization for a word that was rare and ALL CAPS. A larger improvement with a .4 point improvement was noting when a word that was not a number was first in the sentence, instead of marking its specific capitalization. Note that when marking the first word, a quotation mark was not considered as an empty position.

All buckets without first word
------------------------------

Rare word categories/counts:
	'_ALLCAPS_': 758,  '_ALLNUM_': 565,  '_CAPPERIOD_': 63,  '_INITCAP_': 10532,  '_LOWERCASE_': 11167,  '_NUM4D_': 321,  '_NUMALPHA_': 660,  '_NUMCOMMA_': 547,  '_NUMOTHER_': 94,  '_NUMPERIOD_': 1927,  '_NUMSLASH_': 86,  '_RARE_': 1386 

Found 5890 NEs. Expected 5931 NEs; Correct: 4373.

	 precision 	recall 		F1-Score
Total:	 0.742445	0.737312	0.739870
PER:	 0.810112	0.784548	0.797125
ORG:	 0.534994	0.674141	0.596561
LOC:	 0.850336	0.758997	0.802074
MISC:	 0.809403	0.691640	0.745902


No Number Specification
-----------------------

Rare word categories/counts:
	'_ALLCAPS_': 758,  '_CAPPERIOD_': 63,  '_INITCAP_': 10532,  '_LOWERCASE_': 11167,  '_NUMOTHER_': 4897,  '_RARE_': 1386 

Found 5890 NEs. Expected 5931 NEs; Correct: 4375.

	 precision 	recall 		F1-Score
Total:	 0.742784	0.737650	0.740208
PER:	 0.810112	0.784548	0.797125
ORG:	 0.536180	0.675635	0.597884
LOC:	 0.850336	0.758997	0.802074
MISC:	 0.809403	0.691640	0.745902


All CAPS -> lowercase or init_caps if exist already
----------------------------------------------------------------

Rare word categories/counts:
	'_ALLCAPS_': 903,  '_CAPPERIOD_': 63,  '_INITCAP_': 10747,  '_LOWERCASE_': 11300,  '_NUMOTHER_': 4897,  '_RARE_': 1386 

Found 5851 NEs. Expected 5931 NEs; Correct: 4365.

	 precision 	recall 		F1-Score
Total:	 0.746026	0.735964	0.740961
PER:	 0.810325	0.785637	0.797790
ORG:	 0.535842	0.670404	0.595618
LOC:	 0.845449	0.754635	0.797465
MISC:	 0.844327	0.694897	0.762359

First word indication
---------------------

Rare word categories/counts:
	'_ALLCAPS_': 625,  '_CAPPERIOD_': 63,  '_FIRSTWORD_': 2466,  '_INITCAP_': 8887,  '_LOWERCASE_': 11268,  '_NUMOTHER_': 4897,  '_RARE_': 1304 

Found 5871 NEs. Expected 5931 NEs; Correct: 4396.

	 precision 	recall 		F1-Score
Total:	 0.748765	0.741190	0.744958
PER:	 0.837917	0.779108	0.807443
ORG:	 0.528428	0.708520	0.605364
LOC:	 0.853674	0.747546	0.797093
MISC:	 0.846457	0.700326	0.766488


First words -> lowercase or initial capitalization, like the ALL CAPS
---------------------------------------------------------------------

Rare word categories/counts:
	'_ALLCAPS_': 625,  '_CAPPERIOD_': 55,  '_INITCAP_': 10155,  '_LOWERCASE_': 11341,  '_NUMOTHER_': 4897,  '_RARE_': 1711,  '_SOLOCAP_': 22

Found 5527 NEs. Expected 5931 NEs; Correct: 4310.

	 precision 	recall 		F1-Score
Total:	 0.779808	0.726690	0.752313
PER:	 0.843288	0.775843	0.808161
ORG:	 0.584605	0.630045	0.606475
LOC:	 0.853121	0.760087	0.803922
MISC:	 0.851316	0.702497	0.769780
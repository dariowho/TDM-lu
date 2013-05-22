from lu import ChunkedChunk

import lu.ml

from math import log

def c_aavg(score,C_F,C_T,table):
	max_scores = []
	
	# 1 vs 2 comparison: consider both in the average
	if len(C_F) == 1:
		for ct_j in C_T:
			max_scores.append(table.get_score(C_F[0],ct_j))
	# 2 vs X comparison: pick the best
	else:
		for cf_i in C_F:
			max_i = table.get_score(cf_i,C_T[0])
			for ct_j in C_T:
				if table.get_score(cf_i,ct_j).get_score() > max_i.get_score():
					max_i = table.get_score(cf_i,ct_j)
			max_scores.append(max_i)
		
		
	# TEMP CODE to save the chunking hierarchy
	s_from_tree = ChunkedChunk()
	for cf_i in C_F:
		max_i = table.get_score(cf_i,C_T[0])
		for ct_j in C_T:
			if table.get_score(cf_i,ct_j).get_score() > max_i.get_score():
				max_i = table.get_score(cf_i,ct_j)
		s_from_tree.append(max_i.s_from_tree)
	#~ score.s_from = s_from
	score.s_from_tree = s_from_tree
	
	s_to_tree = ChunkedChunk()
	for ct_j in C_T:
		max_j = table.get_score(C_F[0],ct_j)
		for cf_i in C_F:
			if table.get_score(cf_i,ct_j).get_score() > max_j.get_score():
				max_j = table.get_score(cf_i,ct_j)
		s_to_tree.append(max_j.s_to_tree)
	#~ score.s_to = s_to
	score.s_to_tree = s_to_tree
	
	_r = 0.0
	n = 0.0
	for s in max_scores:
		#~ print(s)
		#~ print(s.features)
		#~ print(s.weights)
		#~ print(s.is_feature_set)
		_r = _r + s.get_score()
		n = n+1.0

	_r = _r/n
		
	score.set_feature(score.AAVG,_r)

def c_len(score,C_F,C_T,table):
	# _r = log(min(C_F.length,C_T.length))
	
	l=min(C_F.length,C_T.length)
	import math
	_r = 1-(1.0/(l+0.5))
	
	score.set_feature(score.LEN,_r*score.features[score.AAVG])

#~ def c_len(score,C_F,C_T,table):
	#~ """
	#~ -no description-
	#~ """
#~ 
	#~ # Get the best scores (This is a repetition of the code in the first feature,
	#~ # should be avoided...)
	#~ max_scores = []
	#~ min_len    = []
	#~ for cf_i in C_F:
		#~ max_i = table.get_score(cf_i,C_T[0])
		#~ min_j = C_T[0]
		#~ for ct_j in C_T:
			#~ if table.get_score(cf_i,ct_j).get_score() > max_i.get_score():
				#~ max_i = table.get_score(cf_i,ct_j)
				#~ min_j = ct_j
		#~ max_scores.append(max_i)
		#~ min_len.append( min(cf_i.length,min_j.length) )
		#~ 
	#~ n = 0.0
	#~ _r = 0.0
	#~ for n,i in enumerate(min_len):
		#~ _r = _r+log(i)*max_scores[n].get_score()
		#~ n=n+1.0
	#~ _r=_r/n
	#~ 
	#~ score.set_feature(score.LEN,_r)

def c_ml_afreq(score,C_F,C_T,table):
	"""
	Get a score based on the Alignment Likelihood, as it was learned from 
	previous examples.
	
	TODO: the score is given for the original c_f,c_t (same score for every
	      split of the two). This is inefficient because 1) requires merging
	      C_F,C_T into their original form 2) computes the same result for all
	      the possible splits of c_f,c_t (and this is an expensive computation)
	"""
	
	score.set_feature(score.ML_AFREQ,lu.ml.get_alignment_score(C_F.merge(),C_T.merge()))
	

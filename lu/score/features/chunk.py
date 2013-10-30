# -*- coding: utf-8 -*-

"""
Chunk Score feature computation hooks

NOTE: see lu/score/chunk.py for explanations about the TODO-TMP-CHUNKER label
"""

from lu import ChunkedChunk

import lu.ml

from math import log

def c_aavg(score,C_F,C_T,table):
	"""
	Arithmetic average of the scores of the aligned sub-chunks
	"""
	
	if score.alignment is None:
		_align(score,C_F,C_T,table)
	
	_r = 0.0
	n = 0.0
	for s in score.alignment:
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
	#~ if score.alignment is None:
		#~ _align(score,C_F,C_T,table)
		#~ 
	#~ n = 0.0
	#~ _r = 0.0
	#~ for n,i in enumerate(min_len):
		#~ _r = _r+log(i)*score.alignment[n].get_score()
		#~ n=n+1.0
	#~ _r=_r/n
	#~ 
	#~ score.set_feature(score.LEN,_r)

def c_straight(score,C_F,C_T,table):
	"""
	1 if the alignment is straight (i.e. f1→t1,f2→t2)
	0.5 if the alignment is partially crossed (eg. f1→t1,f2→t1)
	0 if crossed (i.e. f1→t2,f2→t1)
	
	NOTE: this feature is precomputed by the align function
	"""

	if score.alignment is None:
		_align(score,C_F,C_T,table)


def c_ml_afreq(score,C_F,C_T,table):
	"""
	Get a score based on the Alignment Likelihood, as it was learned from 
	previous examples.
	
	TODO-OPT: the score is given for the original c_f,c_t (same score for every
	          split of the two). This is inefficient because 1) requires
	          merging C_F,C_T into their original form 2) computes the same
	          result for all the possible splits of c_f,c_t (and this is an
	          expensive computation)
	"""
	
	#~ score.set_feature(score.ML_AFREQ,lu.ml.get_alignment_score(C_F.merge(),C_T.merge()))
	score.set_feature(score.ML_AFREQ,lu.ml.get_alignment_frequency_norm(C_F.merge(),C_T.merge()))

def c_ml_cfreq(score,C_F,C_T,table):
	"""
	Average of the normalized frequency of c_f and c_t in the language
	
	TODO-OPT: merging required
	"""
	
	_r = lu.ml.get_c_frequency_norm(C_F.merge()) + lu.ml.get_c_frequency_norm(C_T.merge())
	
	score.set_feature(score.ML_CFREQ,_r)

def c_tmp_chunker(score,C_F,C_T,table):
	"""
	TODO-TMP-CHUNKER
	
	Returns 1 only if C_F, C_T, and all of their sub-phrases are present in the
	corpus-based chunk list, 0 otherwise. 
	"""
	
	_r = 1
	
	for c in C_F:
		if c.text.lower() not in table.tmp_chunks_from:
			_r = 0
	
	for c in C_T:
		if c.text.lower() not in table.tmp_chunks_to:
			_r = 0
	
	score.set_feature(score.TMP_CHUNKER,_r)

#
# Private functions
#

def _align(score,C_F,C_T,table):
	"""
	Finds the best alignment for the two chunks being scored.
	
	The result, saved in 'score.alignment' is always a list of two Scores. Two
	options are possible:
	   - C_F contains one element. In this case:
	        score.alignment[0] = Score(C_F[0],C_T[1])
	        score.alignment[1] = Score(C_F[0],C_T[2])
	   - C_F contains two elements. In this case:
	        score.alignment[0] = max(Score(C_F[0],C_T[i]))
	        score.alignment[1] = max(Score(C_F[1],C_T[i]))
	
	Also, this function saves the chunk hierarchy producing a nested 
	ChunkedChunk data structure
	
	NOTE: this function precomputes the STRAIGHT feature
	"""
	
	"""Find the best alignment"""
	score.alignment = []
	
	# 1 vs 2 comparison: consider both in the average
	if len(C_F) == 1:
		for ct_j in C_T:
			score.alignment.append(table.get_score(C_F[0],ct_j))
		straight = 0.5
	# 2 vs X comparison: pick the best
	else:
		#~ for i,cf_i in enumerate(C_F):
			#~ max_i = table.get_score(cf_i,C_T[0])
			#~ straight = 1
			#~ for j,ct_j in enumerate(C_T):
				#~ if table.get_score(cf_i,ct_j).get_score() > max_i.get_score():
					#~ max_i = table.get_score(cf_i,ct_j)
					#~ 
					#~ assert (i==0 and j==1) or (i==1 and j==0)
					#~ straight -= 0.5
			
			try:
				_s1 = table.get_score(C_F[0],C_T[0])
				_s2 = table.get_score(C_F[0],C_T[1])
				if _s1.get_score() > _s2.get_score():
					score.alignment.append(_s1)
					straight = 1
				else:
					score.alignment.append(_s2)
					straight = 0.5
			except IndexError:
				assert len(C_T)==1
				score.alignment.append(_s1)
				straight = 1
			
			try:
				_s1 = table.get_score(C_F[1],C_T[0])
				_s2 = table.get_score(C_F[1],C_T[1])
				if _s1.get_score() > _s2.get_score():
					score.alignment.append(_s1)
					straight -= 0.5
				else:
					score.alignment.append(_s2)
			except IndexError:
				assert len(C_T)==1
				score.alignment.append(_s1)
				straight -= 0.5
			
	score.set_feature(score.STRAIGHT,straight)
		
	"""Save the chunking hierarchy"""
	s_from_tree = ChunkedChunk()
	for cf_i in C_F:
		max_i = table.get_score(cf_i,C_T[0])
		for ct_j in C_T:
			if table.get_score(cf_i,ct_j).get_score() > max_i.get_score():
				max_i = table.get_score(cf_i,ct_j)
		s_from_tree.append(max_i.s_from_tree)
	score.s_from_tree = s_from_tree
	
	s_to_tree = ChunkedChunk()
	for ct_j in C_T:
		max_j = table.get_score(C_F[0],ct_j)
		for cf_i in C_F:
			if table.get_score(cf_i,ct_j).get_score() > max_j.get_score():
				max_j = table.get_score(cf_i,ct_j)
		s_to_tree.append(max_j.s_to_tree)
	score.s_to_tree = s_to_tree

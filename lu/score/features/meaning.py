from lu.score import chunk as chunk_score

import lu.ml

def c_max_sscore(score,meaning_in,sentence_in):
	"""
	Maximum of the sentence scores
	"""
	
	_sentence_similarity_features(score,meaning_in,sentence_in)


def c_avg_sscore(score,meaning_in,sentence_in):
	"""
	Average of the sentence scores
	"""
	
	raise NotImplementedError

def c_ml_ccsum(score,meaning_in,sentence_in):
	"""
	Sum of the class-conditional probabilities of all the chunks in s

	TODO-OPT: recursion is based on the not-optimized split() operation
	"""
	
	score.set_feature(score.ML_CCSUM,_ccsum_compute(sentence_in,meaning_in))

#
# Private procedures
#

def _sentence_similarity_features(score,meaning_in,sentence_in):
	"""
	Aggregate function, computes all the features concerning the meaning's 
	sentence similarities
	"""
	
	max_score_value = 0.0
	sum_scores = 0.0
	for s in meaning_in.sentences:
		s_score = chunk_score.get_score_m2(sentence_in,s)
		s_score_value = s_score.get_score()
		
		# Max score
		if s_score_value > max_score_value:
			max_score_value = s_score_value
			
		# Sum (for average)
		sum_scores = sum_scores + s_score_value
		
		# Save Score debug information
		score.s_sscores.append(s_score)
	
	score.set_feature(score.MAX_SSCORE,max_score_value)
	score.set_feature(score.AVG_SSCORE,sum_scores/len(meaning_in.sentences))


def _ccsum_compute(c,m):
	"""Base case, no need for further recursion"""
	if c.is_word():
		return lu.ml.get_cc_frequency(c,m)
	
	r = 0.0
	"""Handles all the left-splits
	   (including the whole chunk)"""
	for i in range(1,c.length+1):
		_s = c.split(i)
		
		r += lu.ml.get_cc_frequency(_s[0],m)
	
	"""Recursion on the biggest right-split"""
	_s = c.split(1)
	r += _ccsum_compute(_s[1],m)
	
	return r

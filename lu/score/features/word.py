# -*- coding: utf-8 -*-

import sys

from nltk import tokenize,distance
from nltk.corpus import wordnet as wn

def c_equals(score,word_from,word_to,ml):
	"""
	Equality (Boolean).
	"""
	
	if word_from == word_to:
		_r = 1
	else:
		_r = 0
	
	score.set_feature(score.EQUALS,_r)
	
	# Precompute possibly implied features
	if _r == 1:
		score.set_feature(score.EDIT_DISTANCE,1)
		score.set_feature(score.WN_MAX_PATH_SIMILARITY,1)
		
def c_edit_distance(score,word_from,word_to,ml):
	"""
	Inverse of edit distance.
	
	This feature can be precomputed by EQUALS.
	"""

	d = float(distance.edit_distance(word_from.text,word_to.text) + 1)
	_r = 1.0/d
	
	score.set_feature(score.EDIT_DISTANCE,_r)

def c_position_distance(score,word_from,word_to,ml):
	"""
	1 if the words are in the same position in the sentence. The more the 
	distance, the less the score.
	
	TODO: find some nice formula for this (eg. IBM models&co)
	"""
	
	_r = pow( 1.0/float(abs(word_to.position-word_from.position)+1),2 )
	
	score.set_feature(score.POSITION_DISTANCE,_r)

def c_wn_max_path_similarity(score,word_from,word_to,ml):
	"""
	WordNet path similarity for the most similar synsets. (1 if same word)
	
	This feature can be precomputed by EQUALS
	"""
	
	# Enforce returning 1 when words are equal (would be 0 if synset not found)
	# NOTE: since EQUALS precomputes this feature, the assignment in the second
	#       if is double. It is mantained to keep the indipendence on the imple-
	#       mentation of EQUALS.
	if not score.is_feature_set[score.EQUALS]:
		c_equals(score,word_from,word_to)
	if score.features[score.EQUALS] == 1:
		score.set_feature(score.WN_MAX_PATH_SIMILARITY,1)
		return
	
	# Compute the actual distance
	_r = 0
	
	for ss_from in wn.synsets(word_from.text):
		for ss_to in wn.synsets(word_to.text):
			current_similarity = ss_to.path_similarity(ss_from)
			if current_similarity > _r:
				_r = current_similarity
	
	score.set_feature(score.WN_MAX_PATH_SIMILARITY,_r)

def c_ml_afreq(score,word_from,word_to,ml):
	"""
	Get a score based on the Alignment Likelihood, as it was learned from 
	previous examples.
	"""
	
	score.set_feature(score.ML_AFREQ,ml.get_alignment_score(word_from,word_to))

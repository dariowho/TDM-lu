# -*- coding: utf-8 -*-

from array import array

from . import Score
import features.meaning

#
# The WordScore data structure
# NOTE: parent cless Score is defined in __init__.py
#

class MeaningScore(Score):
	"""
	Holds the score of a Sentence against a Meaning.
	"""

	# Total number of features
	N_FEATURES = 2

	# Constant feature names (must define N_FEATURES names)
	MAX_SSCORE, \
	AVG_SSCORE, = range(N_FEATURES)

	def __init__(self,meaning_in,sentence_in):
		super(MeaningScore,self).__init__()

		self.features = array('f',[0]*MeaningScore.N_FEATURES)
		self.weights  = array('f',[1.0/MeaningScore.N_FEATURES]*MeaningScore.N_FEATURES)
		self.is_feature_set = array('b',[False]*MeaningScore.N_FEATURES)
		
		# Debug information
		self.meaning   = meaning_in
		self.sentence  = sentence_in
		self.s_sscores = []
	
#
# Hooks (must match the order of the names in WordScore)
#

_f = [ features.meaning.c_max_sscore, \
       features.meaning.c_avg_sscore ]


#
# Main functions
#

def get_score(meaning_in,sentence_in,ml):
	"""
	Scores a sentence against a meaning-
	"""
	
	r = MeaningScore(meaning_in,sentence_in)
	
	for i,f in enumerate(_f):
		if not r.is_feature_set[i]:
			f(r,meaning_in,sentence_in,ml)

	return r

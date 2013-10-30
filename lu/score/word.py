# -*- coding: utf-8 -*-

from array import array

from . import Score
import features.word

#
# The WordScore data structure
# NOTE: parent cless Score is defined in __init__.py
#

class WordScore(Score):

	# Total number of features
	N_FEATURES = 5

	# Constant feature names (must define N_FEATURES names)
	EQUALS, \
	EDIT_DISTANCE, \
	POSITION_DISTANCE, \
	WN_MAX_PATH_SIMILARITY, \
	ML_AFREQ = range(N_FEATURES)

	def __init__(self,s_from,s_to):
		super(WordScore,self).__init__()

		self.features = array('f',[0]*WordScore.N_FEATURES)
		self.weights  = array('f',[1.0/WordScore.N_FEATURES]*WordScore.N_FEATURES)
		self.is_feature_set = array('b',[False]*WordScore.N_FEATURES)
		
		self.s_from = self.s_from_tree = s_from
		self.s_to   = self.s_to_tree   = s_to
		
		# Hand-crafted weights
		self.weights  = array('f',[0.3,0.05,0.1,0.15,0.4])

	def get_score(self):
		"""
		HACK the original method to return 1 if chunks are the same. No time to
		work on the features to achieve this
		
		TODO: work on the features to achieve this or something similar
		"""
		
		if self.s_from.text == self.s_to.text:
			return 1.0
		
		return super(WordScore,self).get_score()

#
# Hooks (must match the order of the names in WordScore)
#

_f = [ features.word.c_equals, \
       features.word.c_edit_distance, \
       features.word.c_position_distance, \
       features.word.c_wn_max_path_similarity, \
       features.word.c_ml_afreq ]


#
# Main functions
#

def get_score(chunk_from, chunk_to):
	"""
	Compute similarity features between the two input chunks; returns the 
	corresponding WordScore object.
	
	Features are computed only if they have not already been set in the score
	object. This can happen because, in order to optimize the computation time,
	one feature can determine the value of other features (eg. EQUALS can set 
	EDIT_DISTANCE to 1 when the two chunks are the same: there is no need to 
	actually compute the edit distance...)
	"""
	r = WordScore(chunk_from,chunk_to)
	
	for i,f in enumerate(_f):
		if not r.is_feature_set[i]:
			f(r,chunk_from,chunk_to)

	return r

def compute_feature(i,chunk_from,chunk_to):
	return _f[i](chunk_from,chunk_to)

def set_weights():
	"""
	Set the feature weights. Tipically these are values that have been 
	previously estimated with Machine Learning
	"""
	raise NotImplementedError
	
def load_weights():
	"""
	Load the current weights from a file
	"""
	raise NotImplementedError

def save_weights():
	"""
	Saves the current weights to file
	"""
	raise NotImplementedError

def estimate_weights():
	"""
	Estimates the weights of the single features using a development set
	"""
	raise NotImplementedError

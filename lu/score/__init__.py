# -*- coding: utf-8 -*-

"""
The component of the language module that scores the similarity between entities
(meanings, sentences, chunks) in the language.
"""

from array import array

S_OK     = 0
S_EMPTY  = 1
S_BROKEN = 2

__all__ = ["chunk"]

class Score(object):
	
	"""
	The Score data structure holds a similarity score between two entities, 
	keeping the costituents of the score itself (the single features).
	"""
	
	#
	# Meta-methods
	#
	
	def __init__(self):
		features       = array('f',[])
		weights        = array('f',[])
		is_feature_set = array('b',[])
		
		self.status = S_EMPTY
	
	def validate(self):
		"""
		Checks the consistency of the object (features and weights must agree 
		in number)
		"""
		
		if len(self.features) == len(self.weights) == len(self.is_feature_set):
			if len(self.features) > 0:
				self.status = S_OK
				return True
			else:
				self.status = S_EMPTY
				return False
		else:
			self.status = S_BROKEN
			return False
	
	#
	# Core methods
	#
	
	def get_score(self):
		"""
		Computes the total score as the weighted sum of the single features
		
		TODO: maybe cache the result for multiple uses: it is not supposed to 
		      change anyways...
		"""
		r = 0
		
		for i in range(len(self.features)):
			assert self.is_feature_set[i] == True
			r = r + (self.features[i]*self.weights[i])
			
		return r

	#
	# Service methods
	#
	
	def set_feature(self,i,value):
		"""
		Sets the 'i'-th feature to value. 'i' should be referred by a constant,
		defined in the proper subclass of Score.
		"""
		self.features[i]       = value
		self.is_feature_set[i] = True

	def get_feature(self,i):
		"""
		Gets the value of the 'i'-th feature. 'i' should be referred by a
		constant, defined in the proper subclass of Score.
		"""
		assert self.is_feature_set[i]
		
		return self.features[i]

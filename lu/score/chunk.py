# -*- coding: utf-8 -*-

from array import array

from . import Score,word
from lu import ChunkedChunk,Chunk
import features.chunk

# DEBUG
#~ d_recursion_level = 0

class ChunkScore(Score):
	"""
	A ChunkScore holds the score of the comparison of two Chunks.
	"""
	
	# Total number of features
	N_FEATURES = 2
	
	# Constant feature names (must define N_FEATURES names)
	AAVG = 0
	LEN  = 1

	def __init__(self):
		super(ChunkScore,self).__init__()

		self.features = array('f',[0]*ChunkScore.N_FEATURES)
		self.weights  = array('f',[1.0/ChunkScore.N_FEATURES]*ChunkScore.N_FEATURES)
		self.is_feature_set = array('b',[False]*ChunkScore.N_FEATURES)

		# Debug information
		self.s_from  = Chunk("__EMPTY_CHUNK_FROM__",1)
		self.s_to    = Chunk("__EMPTY_CHUNK_TO__",1)
		self.s_table = None

# Hooks (must match the order of the names in WordScore)
_f = [ features.chunk.c_aavg, \
       features.chunk.c_len ]

class M2Table(object):
	"""
	A M2Table object holds a partially precomputed M2-score relation between 
	two chunks
	"""
	
	def __init__(self,chunk_from,chunk_to):
		
		# DEBUG
		#~ print("T_dim: "+str(chunk_from.length)+"x"+str(chunk_from.length)+"x"+str(chunk_to.length)+"x"+str(chunk_to.length) )
		
		# TODO: change this with an optimized matrix
		self.table = [[[[None for x in xrange(chunk_to.length)] for x in xrange(chunk_to.length)] for x in xrange(chunk_from.length)] for x in xrange(chunk_from.length)]
		self.chunk_from = chunk_from
		self.chunk_to   = chunk_to
	
	def set_score(self,score,chunk_from,chunk_to):
		assert self.table[chunk_from.position-1][chunk_from.position+chunk_from.length-2][chunk_to.position-1][chunk_to.position+chunk_to.length-2] is None
		
		self.table[chunk_from.position-1][chunk_from.position+chunk_from.length-2][chunk_to.position-1][chunk_to.position+chunk_to.length-2] = score

	def get_score(self,chunk_from,chunk_to):
		assert self.table[chunk_from.position-1][chunk_from.position+chunk_from.length-2][chunk_to.position-1][chunk_to.position+chunk_to.length-2] is not None
		
		return self.table[chunk_from.position-1][chunk_from.position+chunk_from.length-2][chunk_to.position-1][chunk_to.position+chunk_to.length-2]
	
	def is_score_set(self,chunk_from,chunk_to):
		# DEBUG
		#~ global d_recursion_level
		#~ print("\t"*d_recursion_level+"T_isset: from: "+str(chunk_from.position)+","+str(chunk_from.length))
		#~ print("\t"*d_recursion_level+"T_isset: to  : "+str(chunk_to.position)+","+str(chunk_to.length))
		
		return self.table[chunk_from.position-1][chunk_from.position+chunk_from.length-2][chunk_to.position-1][chunk_to.position+chunk_to.length-2] is not None

def get_score_m2(chunk_from,chunk_to):
	"""
	Runs the actual score computing function, initialized with an empty M2Table
	"""

	# Note that, even though it is only useful for debug purposes, the last 
	# score is pushed into the table (which will be accessible through the
	# ChunkScore object)
	table = M2Table(chunk_from,chunk_to)
	r = _get_score_m2(chunk_from,chunk_to,table)
	table.set_score(r,chunk_from,chunk_to)
	
	return r

def _get_score_m2(chunk_from,chunk_to,table):
	"""
	This function scores the similarity between two chunks using the M2-score
	algorithm.
	
	This algorithm makes use of Dynamic Programming to reduce the computation 
	time, still comparing every possible alignment of every possible 
	sub-chunking of the two input chunks.
	
	'chunk_from' and 'chunk_to' are two Chunk object. 'table' is a M2Table
	object, representing the partially precomputed M2-score relation. This 
	table, initially empty, gets filled as the algorithm runs; in the end it
	will contain all the partial scores (one ChunkScore object for each possible
	combination of sub-chunking of chunk_from and chunk_to).
	"""
	
	
	# DEBUG
	#~ global d_recursion_level
	#~ print("\t"*d_recursion_level+"M2: '"+chunk_from.text+"','"+chunk_to.text+"'")
	#~ print("\t"*d_recursion_level+"    '"+str(chunk_from.length)+"','"+str(chunk_to.length)+"'")
	#~ print("\t"*d_recursion_level+"    '"+str(chunk_from.position)+"','"+str(chunk_to.position)+"'")
	#~ d_recursion_level = d_recursion_level+1
	
	if chunk_from.is_word() and chunk_to.is_word():
		# DEBUG
		#~ print("word score returned")
		#~ d_recursion_level = d_recursion_level-1
		
		# TODO: The two ChunkedChunks that are being compared are saved in
		#       the Score. Coding style apart, this shouldn't affect the
		#       performance too much; anyway, it would be better to check.
		#       See also the feature hook.
		r = word.get_score(chunk_from,chunk_to)
		r.s_from = chunk_from
		r.s_to   = chunk_to
		return word.get_score(chunk_from,chunk_to)
	
	# TODO: precompute the size
	candidate_scores = []
	
	# For every 2-split of 'chunk_from'
	for i in range(1,chunk_from.length+1):
		C_F = chunk_from.split(i)
		
		# For every 2-split of 'chunk_to'
		for j in range(1,chunk_to.length+1):
			
			# Prevent infinite loops
			# DEBUG
			#~ print ("\t"*d_recursion_level+"i:"+str(i)+","+str(chunk_from.length))
			#~ print ("\t"*d_recursion_level+"j:"+str(j)+","+str(chunk_to.length))
			if (i == chunk_from.length) and (j == chunk_to.length) and \
			   (i != 1 or j != 1):
				# DEBUG
				#~ print("Infinite loop prevented")
				break
			
			C_T = chunk_to.split(j)
			
			# Compute the scores of every possible alignment, if not done yet
			# NOTE: C_F and C_T are list of chunks or words; typically they
			#       contain 2 chunks (the 2-split of chunk_*), but it can also 
			#       be one (when the entire chunk_* is compared with the 
			#       sub-chunks of the other) 
			for cf_i in C_F:
				for ct_j in C_T:
					if not table.is_score_set(cf_i,ct_j):
						# DEBUG
						#~ print("score("+str(cf_i.text)+","+str(ct_i.text)+")")
						table.set_score(_get_score_m2(cf_i,ct_j,table),cf_i,ct_j)
					# DEBUG
					#~ else:
						#~ print("HIT! "+cf_i.text+","+ct_i.text)
			
			#~ print("-------------------------------------------")
			
			# Compute the score for chunk_from and chunk_to, under this 
			# particular sub-chunking. This score is added to the list of
			# candidate scores; the best score (ie. the best sub-chunking) will
			# be selected in the end
			# NOTE: it is up to the score to handle the alignment of the 
			#       sub-chunks in the two sentences
			score = ChunkScore()
			score.s_table = table
			for fn,f in enumerate(_f):
				if not score.is_feature_set[fn]:
					f(score,C_F,C_T,table)
			candidate_scores.append(score)
			
			# DEBUG
			#~ print score
	
	# DEBUG
	#~ print(candidate_scores)
	
	# Return the best score
	max_score = candidate_scores[0]
	for s in candidate_scores:
		if s.get_score() > max_score.get_score():
			max_score = s
			
	#DEBUG
	#~ d_recursion_level = d_recursion_level-1
	
	return max_score


# TODO: this function is never used!
def _get_chunk_score_m2(C_F,C_T,table):
	score = ChunkScore()
	score.s_table = table
	for fn,f in enumerate(_f):
		if not score.is_feature_set[fn]:
			f(score,C_F,C_T,table)
	return score
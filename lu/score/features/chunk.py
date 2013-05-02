from lu import ChunkedChunk

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
	s_from = ChunkedChunk()
	for cf_i in C_F:
		max_i = table.get_score(cf_i,C_T[0])
		for ct_j in C_T:
			if table.get_score(cf_i,ct_j).get_score() > max_i.get_score():
				max_i = table.get_score(cf_i,ct_j)
		s_from.append(max_i.s_from)
	score.s_from = s_from
	
	s_to = ChunkedChunk()
	for ct_j in C_T:
		max_j = table.get_score(C_F[0],ct_j)
		for cf_i in C_F:
			if table.get_score(cf_i,ct_j).get_score() > max_j.get_score():
				max_j = table.get_score(cf_i,ct_j)
		s_to.append(max_j.s_to)
	score.s_to = s_to
	
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

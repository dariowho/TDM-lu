from lu.score import chunk as chunk_score

def c_max_sscore(score,meaning_in,sentence_in,ml):
	"""
	Maximum of the sentence scores
	"""
	
	_sentence_similarity_features(score,meaning_in,sentence_in,ml)


def c_avg_sscore(score,meaning_in,sentence_in,ml):
	"""
	Average of the sentence scores
	"""
	
	raise NotImplementedError

#
# Private procedures
#

def _sentence_similarity_features(score,meaning_in,sentence_in,ml):
	"""
	Aggregate function, computes all the features concerning the meaning's 
	sentence similarities
	"""
	
	max_score_value = 0.0
	sum_scores = 0.0
	for s in meaning_in.sentences:
		s_score = chunk_score.get_score_m2(sentence_in,s,ml)
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

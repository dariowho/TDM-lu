# -*- coding: utf-8 -*-

import lu.ml
import lu.score.chunk

def learn(sentence_in,meaning_in,m2tables = None):
	"""
	Updates Machine Learning knowledge of the language with the given example
	"""

	"""Update chunk/class-conditional frequencies"""
	_process_chunks(sentence_in,meaning_in)
	
	"""If no score tables are given, compute them"""
	if m2tables is None:
		m2tables = []
		for s in meaning_in.sentences:
			_s = lu.score.chunk.get_score_m2(sentence_in,s)
			assert _s is not None
			m2tables.append(_s.s_table)
			
	assert len(m2tables) == len(meaning_in.sentences)
	
	"""Update alignment frequencies with table scores"""
	for t in m2tables:
		_process_m2table(t)
	
def _process_chunks(sentence_in,meaning_in):
	"""
	Update chunk count and class-conditional count for the input Sentence
	(Chunk) and, recursively, all of its components.
	
	TODO-OPT: recursion is based on the not-optimized split() operation
	"""
	
	"""Base case, no need for further recursion"""
	if sentence_in.is_word():
		lu.ml.increment_c_frequency(sentence_in)
		lu.ml.increment_cc_frequency(sentence_in,meaning_in)
		
		return
	
	"""Handles all the left-splits
	   (including the whole chunk)"""
	for i in range(1,sentence_in.length+1):
		_s = sentence_in.split(i)
		
		lu.ml.increment_c_frequency(_s[0])
		lu.ml.increment_cc_frequency(_s[0],meaning_in)
	
	"""Recursion on the biggest right-split"""
	_s = sentence_in.split(1)
	_process_chunks(_s[1],meaning_in)

def _process_m2table(m2table):
	"""
	Update alignment frequencies using the scores in the given table
	"""
	
	for from_a in m2table.table:
		for from_b in from_a:
			for to_a in from_b:
				for to_b in to_a:
					if to_b is not None:
						lu.ml.reinforce_alignment(to_b.s_from,to_b.s_to,to_b.get_score())

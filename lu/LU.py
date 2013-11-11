# -*- coding: utf-8 -*-

"""
LANGUAGE UNIT - Classes and functions for handling language
===========================================================

The purpose of this package is to load a language, understand sentences of the
language, and incrementally learn the language through experience.

A language is here defined by a set of sentences, each of them is labeled with
a logical form. To understand a sentence means to associate it to its logical
form. This can happen in two ways:
 - The sentence is already existing in the memorized language
 - The sentence is considered semantically affine to a particular label.
Unrecognized sentences, once understood, can be used to enrich the system's
knowledge of the language.
"""

import sys

from array import array

from . import Meaning,Sentence,Chunk,ChunkedChunk,Word
from constants import *

import lu.ml

import learn.sentence
import learn.interaction

import score.chunk
import score.word
import score.meaning
import score.output.meaning

import datetime
now = datetime.datetime.now()
__version__ = "dev-"+str(now.year)+str(now.month)+str(now.day)

"""
Constants
"""

# Tuple elements of Language.understand() return value
U_LABEL   = 0
U_SCORE_F = 1
U_SCORE   = 2

# Extra elements in case of TDM-specific understanding (see learn.interaction)
U_QUESTIONS = 3

"""
The Language class
"""

class Language:
	# Status
	_valid   = False
	_status  = STATUS.EMPTY
	
	# Training language
	sentence = []
	label    = []
	weight   = []
	
	# Language indexed by meaning
	meaning = []
	m_label = []
	
	#
	# Meta-methods
	#

	def __init__(self):
		self._valid  = False
		self._status = STATUS.EMPTY
		
	def validate(self):
		"""
		Check the language is consistent (should always be...)
		
		TODO: implement
		"""
		
		self._status = STATUS.OK
		return True

	#
	# Core methods
	#

	def understand(self,sentence_in):
		"""
		Assign an input sentence to one of the labels of the language, perfor-
		ming a semantic match.
		
		Returns a list of tuples (label,score) ordered by score. Scores are
		malized so that their score head up to 1.
		
		NOTE: Implementation is being changed, lists may be chosen instead of 
		      tuples
		"""

		r = []
		scores_sum = 0.0

		for i in range(len(self.meaning)):
			s = score.meaning.get_score(self.meaning[i],Sentence(sentence_in))
			
			score_f = s.get_score()
			r.append( [self.meaning[i].label,score_f,s] )
		
			scores_sum += score_f
			
		r.sort(key=lambda t: t[1], reverse=True)
		
		# HACK: bypass everything if top score is 1 (i.e. exact sentence match)
		if r[0][U_SCORE_F] == 1:
			return [ r[0] ]
		# END HACK
		
		for s in r:
			s[U_SCORE_F] = s[U_SCORE_F]/scores_sum
		
		# DEBUG
		print("\n[LU.Language] understand(): Printing debug output")
		for s in r:
			print(s)
		print("[LU.Language] understand(): End debug output\n")
		# END DEBUG
		
		return learn.interaction.get_plan_tdm(r)

			
	def learn(self,sentence_text_in,meaning_label_in):
		"""
		Extend the knowledge about the language from a labeled example
		"""
		
		s = Sentence(sentence_text_in)
		m = self.meaning[ self.m_label.index(meaning_label_in) ]
		learn.sentence.learn(s,m)
	
	def solve_top_ground_issue(self,result):
		"""
		Solves the top element in the open grounding hypotheses stack (see 
		learn.interaction)
		
		NOTE: temp method for thesis purposes only
		"""
		
		if result == 1:
			_tmp = "positive"
		else:
			_tmp = "negative"
		
		hypothesis = learn.interaction.tdm_ground_stack.pop()
		
		# TODO: implement
		print(u"\n[LU.Language] solve_top_ground_issue() Solving "+unicode(hypothesis)+" as "+_tmp)
		
		return hypothesis[0]
	
	def understand_debug(self,sentence_in):
		"""
		Equal tu understand(), but prints the results on screen as HTML code
		"""

		#~ for _ in range(10):
			#~ for i in range(len(self.meaning)):
				#~ s = score.meaning.get_score(self.meaning[i],Sentence(sentence_in))

		for i in range(len(self.meaning)):
			s = score.meaning.get_score(self.meaning[i],Sentence(sentence_in))
			score.output.meaning.render_html(s)
	
	#
	# Input/Output methods
	#
	
	def load(self,path=None):
		"""
		Load a language from a binary Language file (*.lo, a pickled Python
		class)
		
		TODO: implement (as of now it loads a stub language)
		"""
		
		raise(NotImplementedError)
		
		#~ self.sentence = stub_language.sentence
		#~ self.label    = stub_language.label
		#~ self.weight   = stub_language.weight
	
	def save(self,path):
		"""
		Saves the current language into a binary Language file (*.lo, a pickled
		Python class)
		
		TODO: implement
		"""
		
		raise NotImplementedError
	
	def import_l(self,path,name):
		"""
		Import the language from a human-readable language file (*.l)
		"""
		
		f = open(path+name+".l",'r')
		
		ln = 0
		for line in f:
			ln = ln+1
			
			"""Skip empty lines"""
			if line == "" or not line.strip():
				continue
			
			"""Skip comments"""
			if line[0] == "#":
				continue
			
			"""Parse the line"""
			tokens = line.split('\t')
			try:
				cur_label    = unicode(tokens[FORMAT.P_LABEL])
				cur_weight   = float(tokens[FORMAT.P_WEIGHT])
				cur_sentence = Sentence(unicode(tokens[FORMAT.P_SENTENCE].strip()))
			except:
				# TODO: for some reason it doesn't see the global "import sys": WHY???
				import sys
				sys.stderr.write("LU.Language.import_L(): Error processing line "+unicode(ln)+". Skipping.\n")
				continue
				
			"""Update the general sentence list"""
			self.label.append( cur_label )
			self.weight.append( cur_weight )
			self.sentence.append( cur_sentence )
			
			"""Update the meaning index"""
			if cur_label not in self.m_label:
				self.meaning.append( Meaning(cur_label) )
				self.m_label.append( cur_label )
			m_i = self.m_label.index(cur_label)
			self.meaning[m_i].add_sentence(cur_sentence,cur_weight)
		
		f.close()
			
		"""Initialize Machine Learning values"""
		if lu.ml.ml_data_exist(path,name):
			lu.ml.import_ml(path,name)
		else:
			import sys
			sys.stderr.write("[LU.import_l] ML data not found, building...\n")
			
			for m in self.meaning:
				for s in m.sentences:
					learn.sentence.learn(s,m)
			
			sys.stderr.write("[LU.import_l] ML training finished.\n")
			
			lu.ml.export_ml(path,name)
			
		return True
		
	def export_l(self,path):
		"""
		Export the language into a human-readable language file (*.l)
		"""
		
		f = open(path,'w')
		
		f.write("# This is an automatically generated Language file\n")
		
		# Label [TAB] Weight [TAB] Sentence [NEWLINE]
		for i in range(len(self.sentence)):
			f.write(unicode(self.label[i])+u'\t'+ \
			        unicode(self.weight[i])+u'\t'+ \
			        unicode(self.sentence[i])+u'\n')
		
		f.close()
		
		return True


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
from language_base import stub_language
from ml.core import ML

import score.chunk
import score.word
import score.meaning
import score.output.meaning

import datetime
now = datetime.datetime.now()
__version__ = "dev-"+str(now.year)+str(now.month)+str(now.day)

#
# The Language class
#

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
	
	# Machine Learning Module
	ml = None

	#
	# Meta-methods
	#

	def __init__(self):
		self._valid  = False
		self._status = STATUS.EMPTY
		
		self.ml = ML()
		
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
		ming a semantic match
		"""

		for i in range(len(self.meaning)):
			s = score.meaning.get_score(self.meaning[i],Sentence(sentence_in),self.ml)
		
		for i in range(len(self.meaning)):
			s = score.meaning.get_score(self.meaning[i],Sentence(sentence_in),self.ml)
			score.output.meaning.render_html(s)
			
	def learn(self,sentence_in,meaning_in):
		"""
		Extend the knowledge about the language from a labeled example
		"""
		
		raise NotImplementedError
		
	#
	# Input/Output methods
	#
	
	def load(self,path=None):
		"""
		Load a language from a binary Language file (*.lo, a pickled Python
		class)
		
		TODO: implement (as of now it loads a stub language)
		"""
		
		if path is not None:
			raise(NotImplementedError)
		
		self.sentence = stub_language.sentence
		self.label    = stub_language.label
		self.weight   = stub_language.weight
	
	def save(self,path):
		"""
		Saves the current language into a binary Language file (*.lo, a pickled
		Python class)
		
		TODO: implement
		"""
		
		raise NotImplementedError
	
	def import_l(self,path):
		"""
		Import the language from a human-readable language file (*.l)
		"""
		
		f = open(path,'r')
		
		ln = 0
		for line in f:
			ln = ln+1
			
			# Skip empty lines
			if line == "" or not line.strip():
				continue
			
			# Skip comments
			if line[0] == "#":
				continue
			
			# Parse the line
			tokens = line.split('\t')
			try:
				cur_label    = unicode(tokens[FORMAT.P_LABEL])
				cur_weight   = float(tokens[FORMAT.P_WEIGHT])
				cur_sentence = Sentence(unicode(tokens[FORMAT.P_SENTENCE].strip()))
			except:
				sys.stderr.write("LU.Language.import_L(): Error processing line "+unicode(ln)+". Skipping.\n")
				continue
				
			# Update the general sentence list
			self.label.append( cur_label )
			self.weight.append( cur_weight )
			self.sentence.append( cur_sentence )
			
			# Update the meaning index
			if cur_label not in self.m_label:
				self.meaning.append( Meaning(cur_label) )
				self.m_label.append( cur_label )
			m_i = self.m_label.index(cur_label)
			self.meaning[m_i].add_sentence(cur_sentence,cur_weight)
			
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


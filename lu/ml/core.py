# -*- coding: utf-8 -*-

"""
ML - Machine Learning component for the Language Unit
=====================================================

The purpose of this package is to provide classes and functions to store and
retrieve learned information about the language.

This information includes
   * Frequency count for each chunk
   * Class-conditional probability for each chunk
   * Alignment score for each couple of chunks
   
Some assumptions are made throughout the package, that may or may not need 
future review:
   * Quantities are symmetric (c1,c2)=(c2,c1). This is achieved by ordering
     c1 and c2 alphabetically before accessing the index. Also, when two scores
     are possible, the average is considered.
   * Chunks are indexed by their text content, other properties (eg. position
     in sentence, POS tag, etc.) are ignored.
     
     TODO: it would be nice to implement it replacing Python get/set methods, 
           rather then taking the text from the Chunk in every function
"""

import sys
import math
import os.path

# TODO: update alignment frequency operations to use defaultdict!
from collections import defaultdict

class ML(object):

	DEFAULT_MASS  = 1
	DEFAULT_SCORE = 1
	
	def __init__(self):
		# Chunk frequency (count and mass)
		# TODO: mass is probably useless...
		self.c_count            = defaultdict(int)
		self._c_cache_count_tot = 0
		self.c_mass             = defaultdict(ML._floatdefaultdict_factory)
		self._c_cache_mass_tot  = 0.0
		
		# Class-conditional chunk frequency
		self.cc_count            = defaultdict(ML._intdefaultdict_factory)
		self._cc_cache_count_m   = defaultdict(int)
		self._cc_cache_count_tot = 0
		
		# Alignment frequency
		self.a_mass            = defaultdict(ML._floatdefaultdict_factory)
		self._a_cache_mass_c   = defaultdict(float)
		self._a_cache_mass_tot = 0.0
	
	#
	# Core methods - Chunk count
	#
	
	def get_c_frequency(self,c):
		"""
		(Count of c) / (Total count)
		"""
		c = c.text
		
		try:
			return self.c_count[c]/self._c_cahce_count_tot
		except ZeroDivisionError:
			"""No chunk have been counted yet"""
			return 0
			
	def increment_c_frequency(self,c):
		c = c.text
		
		self.c_count[c] += 1
		
		self._c_cache_count_tot += 1
	
	#
	# Core methods - Class-conditional count
	#
	
	def get_cc_frequency(self,c,m):
		"""
		Given a chunk 'c' and a meaning 'm' returns the count of 'c' in 'm'
		over the total count of chunks in 'm'
		"""
		c = c.text
		m = m.label
		
		try:
			return self.cc_count[c][m]/self._cc_cache_count_m[c]
		except ZeroDivisionError:
			"""No chunks in this meaning have been counted yet"""
			return 0
	
	def increment_cc_frequency(self,c,m):
		c = c.text
		m = m.label
		
		self.cc_count[c][m]       += 1
		self._cc_cache_count_m[m] += 1
		self._cc_cache_count_tot  += 1
	
	#
	# Core methods - Alignments
	#
	
	def get_alignment_score(self,c1,c2):
		"""
		Returns the fraction of c1 mass that is covered by the c1,c2 alignment
		
		NOTE: because of the order-invariant properties of the mass, the result
		      can be given respect to both c1 and c2. The average of the two
		      is returned.
		      
		TODO: consider weighting the results in proportion to the total mass
		      being covered.
		"""
		
		if c1.text == c2.text:
			return 1
		
		m   = self._get_alignment_mass(c1,c2)
		m2  = self._get_alignment_mass(c2,c1)
		tm1 = self._get_alignment_mass(c1)
		tm2 = self._get_alignment_mass(c2)

		assert (tm1 != 0 and tm2 != 0) or (m == 0)

		# DEBUG 
		#~ import sys
		#~ sys.stderr.write("m: "+str(m)+"\n")
		#~ sys.stderr.write("m1: "+str(tm1)+"\n")
		#~ sys.stderr.write("m2: "+str(tm2)+"\n")
			
		try:
			#~ sys.stderr.write("try: "+str(( (m/tm1) + (m2/tm2) ) / 2)+"\n")
			return ( (m/tm1) + (m2/tm2) ) / 2
			#~ return (m/tm1)*(m/tm2)
			#~ return 2*m/(tm1+tm2) # Can be greater than zero
			#~ return m/(tm1)
		except ZeroDivisionError:
			#~ sys.stderr.write("except: "+str(ML.DEFAULT_SCORE)+"\n")
			return ML.DEFAULT_SCORE
		
	def reinforce_alignment(self,c1,c2,score):
		"""
		Different policies are possible:
		   * mass = mass + score
		   * mass = mass + mass*score
		   * mass = mass / score
		   * mass = mass * score
		   * ...
		"""
		
		if c1.text == c2.text:
			return

		assert not math.isnan(score)
		
		m = self._get_alignment_mass(c1,c2)
		#~ self._set_alignment_mass(c1,c2,m+m*score)
		self._set_alignment_mass(c1,c2,m+score)

		m = self._get_alignment_mass(c2,c1)
		#~ self._set_alignment_mass(c2,c1,m+m*score)
		self._set_alignment_mass(c2,c1,m+score)
		
	def discourage_alignment(self,c1,c2,score):
		"""
		TODO: update criterion according to reinforcement policy (operation +
		      simmetry)
		"""
		
		raise NotImplementedError
		
		if c1.text == c2.text:
			return
		
		m = self._get_alignment_mass(c1,c2)
		
		m -= score

		self._set_alignment_mass(c1,c2,m)

	#
	# Input/Output methods
	#

	def ml_data_exist(self,path,name):
		"""
		Check if ml data already exist in the given folder ('path') for the 
		given language ('name')
		
		TODO: some consistency check, maybe hashing the language object, would
		      be sweet...
		"""
		
		path = path+name
		
		return os.path.isfile(path+".ml.cfreq") and \
		       os.path.isfile(path+".ml.ccfreq") and \
		       os.path.isfile(path+".ml.afreq")

	def import_ml(self,path,name):
		"""
		Imports ML data from human-readable .ml files (see 'export_ml' below).
		
		'path' is the path to the directory containing the ml files, including
		       the last slash
		'name' is the name of the language (without any extension)
		
		TODO: the imput procedures don't remove the content that may already be
		      present in the ml's data structures
		"""
		
		path = path+name
		
		self._import_ml_c(path+".ml.cfreq")
		self._import_ml_cc(path+".ml.ccfreq")
		self._import_ml_a(path+".ml.afreq")

	def export_ml(self,path,name):
		"""
		Exports the Machine Learning data into human-readable files:
		   * [path][name].ml.cfreq  - Chunk frequency data
		   * [path][name].ml.ccfreq - Class-conditional chunk frequency data
		   * [path][name].ml.afreq  - Alignment frequency data
		
		'path' is the path to the directory containing the ml files, including
		       the last slash
		'name' is the name of the language (without any extension)
		
		NOTE: the 'item' iterator is used in place of 'iteritems' to loop over
		      the dictionaries. This is to maintain the compatibility with 
		      Python3; on Python2 this causes the whole dictionary to be
		      replicated in the memory instead of be looped on the fly (as it
		      happens with 'iteritems' on py2 and with 'items' on py3), losing
		      efficiency.
		
		TODO: meta-symbols (TAB) are not escaped
		"""
		
		"""Build the full path from path and filename"""
		path = path+name
		
		f_cfreq  = open(path+'.ml.cfreq','w')
		f_ccfreq = open(path+'.ml.ccfreq','w')
		f_afreq  = open(path+'.ml.afreq','w')

		f_cfreq.write(u"# This is an automatically generated ML data file, containing\n"+\
		              u"# chunk frequency data.\n"+\
		              u"# Its content is meant to be updated by a scoring system,\n"+\
		              u"# handmade modifications are likely to break its consistency.\n\n")
		f_ccfreq.write(u"# This is an automatically generated ML data file, containing\n"+\
		               u"# class-conditional chunk frequency data.\n"+\
		               u"# Its content is meant to be updated by a scoring system,\n"+\
		               u"# handmade modifications are likely to break its consistency.\n\n")
		f_afreq.write(u"# This is an automatically generated ML data file, containing\n"+\
		              u"# alignment frequency data.\n"+\
		              u"# Its content is meant to be updated by a scoring system,\n"+
		              u"# handmade modifications are likely to break its consistency.\n\n")

		for k,v in self.c_count.items():
			f_cfreq.write(k+u"\t"+unicode(v)+"\t;\n")
		f_cfreq.write(u"\nT\t"+unicode(self._c_cache_count_tot))
		f_cfreq.close()
		
		for k_i,v_i in self.cc_count.items():
			for k_j,v_j in v_i.items():
				f_ccfreq.write(k_i+u"\t"+k_j+u"\t"+unicode(v_j)+u"\t;\n")
		f_ccfreq.write(u"\n")
		for k,v in self._cc_cache_count_m.items():
			f_ccfreq.write(u"T\t"+k+u"\t"+unicode(v)+u"\n")
		f_ccfreq.write(u"\nT\t"+unicode(self._cc_cache_count_tot))
		f_ccfreq.close()
		
		for k_i,v_i in self.a_mass.items():
			for k_j,v_j in v_i.items():
				f_afreq.write(k_i+u"\t"+k_j+u"\t"+unicode(v_j)+u"\t;\n")
		f_afreq.write(u"\n")
		for k,v in self._a_cache_mass_c.items():
			f_afreq.write(u"T\t"+k+u"\t"+unicode(v)+u"\n")
		f_afreq.write(u"\nT\t"+unicode(self._a_cache_mass_tot))
		f_afreq.close()

	#
	# Private methods - general
	#
	@staticmethod
	def _intdefaultdict_factory():
		"""
		This method is used to set the default value of the class-conditional
		index, wich is a 'defaultdict' having 'int' as an argument.
		(The whole structure is thus a 'defautdict' of 'defaultdict's, see
		__init__)
		"""
		return defaultdict(int)

	@staticmethod
	def _floatdefaultdict_factory():
		"""
		This method is used to set the default value of the mass-based indices
		(eg. alignment), wich is a 'defaultdict' having 'float' as an argument.
		(The whole structure is thus a 'defautdict' of 'defaultdict's, see
		__init__)
		"""
		return defaultdict(float)

	#
	# Private methods - Alignment frequencies
	#
	
	def _get_alignment_mass(self,c1=None,c2=None):
		"""
		_get_alignment_mass()       - Total alignment score mass
		_get_alignment_mass(c)      - Score mass of the alignments involving c
		_get_alignment_mass(c1,c2)  - Score mass of the alignment c1,c2
		
		Returns a default value if c1 or c2 is not in the in the index
		"""
		
		if c1 is None and c2 is None:
			return self._a_cache_mass_tot
		
		assert c1 is not None
		c1 = c1.text
		
		if c2 is None:
			"""NOTE: the 'get' method to get to return the default value in
			         case of miss instead of taking advantage of 'defaultdict'.
			         This is because the default value would be stored in the 
			         dictionary otherwise, adding unexistent mass to c1.
			"""
			return self._a_cache_mass_c.get(c1,ML.DEFAULT_MASS)
		
		c2 = c2.text
		
		#~ if c1 > c2:
			#~ c1,c2 = c2,c1
		
		return self.a_mass.get(c1,dict()).get(c2,ML.DEFAULT_MASS)

	def _set_alignment_mass(self,c1,c2,m):
		"""
		Replaces the current mass value (or creates it, if does not exist) for
		c1,c2 with m, updating the cache of total scores.
		
		Also increments the chunk counts
		
		Note that pointers are used throughout the function to speed up the 
		access to the index:
		   * p_a_mass_c1    = self.a_mass[c1]
		"""
		c1 = c1.text
		c2 = c2.text
		
		# simmetry hack
		#~ if c1 > c2:
			#~ c1,c2 = c2,c1

		p_a_mass_c1 = self.a_mass[c1]

		"""Update direct (c1,c2) value"""
		m_diff = m - p_a_mass_c1[c2]
		p_a_mass_c1[c2] = m
		
		assert self.a_mass[c1][c2] == m
		
		"""Update c1 cache"""
		self._a_cache_mass_c[c1] += m_diff
		#~ self._a_cache_mass_c[c2] += m_diff ← bidirectional update, for simmetry hack

		"""Update total cache"""
		self._a_cache_mass_tot += m_diff

	#
	# Private methods - I/O
	#
	
	def _import_ml_c(self,path):
		f = open(path,'r')
		
		ln = 0
		for line in f:
			ln += 1
			
			"""Skip empty lines"""
			if line == "" or not line.strip():
				continue
			
			"""Skip comments"""
			if line[0] == "#":
				continue
			
			"""Parse the line"""
			tokens = line.split('\t')
			"""Try to parse as a chunk count line (3 elements)"""
			try:
				chunk = unicode(tokens[0])
				count = int(tokens[1])
				col   = tokens[2].strip()
				assert col == ';'
				
				self.c_count[chunk] = count
			except:
				"""Try to parse as a total count line (2 elements)"""
				try:
					if unicode(tokens[0]) != "T":
						raise Exception
						
					self._c_cache_count_tot = int(tokens[1])
				except:
					sys.stderr.write("lu.ml: Error processing ml.cfreq line "+unicode(ln)+". Skipping.\n")
					continue
		
		f.close()
	
	def _import_ml_cc(self,path):
		f = open(path,'r')

		ln = 0
		for line in f:
			ln += 1
			
			"""Skip empty lines"""
			if line == "" or not line.strip():
				continue
			
			"""Skip comments"""
			if line[0] == "#":
				continue
			
			"""Parse the line"""
			tokens = line.split('\t')
			"""Try to parse as a cc count line (4 elements)"""
			try:
				chunk   = unicode(tokens[0])
				meaning = unicode(tokens[1])
				count   = int(tokens[2])
				col     = tokens[3].strip()
				assert col == ';'
				
				self.cc_count[chunk][meaning] = count
			except:
				"""Try to parse as a marginal meaning count line (3 elements)"""
				try:
					if unicode(tokens[0]) != "T":
						raise Exception
					
					meaning = unicode(tokens[1])
					count   = int(tokens[2])
						
					self._cc_cache_count_m[meaning] = count
				except:
					"""Try to parse as a total count line (2 elements)"""
					try:
						if unicode(tokens[0].strip()) != "T":
							raise Exception
						
						self._cc_cache_count_tot = int(tokens[1])
					except:
						sys.stderr.write("lu.ml: Error processing ml.ccfreq line "+unicode(ln)+". Skipping.\n")
						continue

		f.close()
		
	def _import_ml_a(self,path):
		f = open(path,'r')

		ln = 0
		for line in f:
			ln += 1
			
			"""Skip empty lines"""
			if line == "" or not line.strip():
				continue
			
			"""Skip comments"""
			if line[0] == "#":
				continue
			
			"""Parse the line"""
			tokens = line.split('\t')
			"""Try to parse as a cc count line (4 elements)"""
			try:
				chunk_from = unicode(tokens[0])
				chunk_to   = unicode(tokens[1])
				mass       = float(tokens[2])
				col        = tokens[3].strip()
				assert col == ';'
				
				self.a_mass[chunk_from][chunk_to] = mass
			except:
				"""Try to parse as a marginal meaning mass line (3 elements)"""
				try:
					if unicode(tokens[0]).strip() != "T":
						raise Exception
					
					chunk = unicode(tokens[1])
					mass  = float(tokens[2].strip())

					self._a_cache_mass_c[chunk] = mass
				except:
					"""Try to parse as a total mass line (2 elements)"""
					try:
						if unicode(tokens[0]).strip() != "T":
							raise Exception
						
						self._a_cache_mass_tot = float(tokens[1].strip())
					except:
						sys.stderr.write("lu.ml: Error processing ml.afreq line "+unicode(ln)+". Skipping.\n")
						continue

		f.close()

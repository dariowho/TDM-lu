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

import math

class ML(object):

	DEFAULT_MASS  = 1
	DEFAULT_SCORE = 1
	
	def __init__(self):
		# Chunk frequency
		# TODO: distinguish between count and mass
		self.c_mass            = dict()
		self._c_cache_mass_tot = 0.0
		
		# Class-conditional chunk frequency
		# NOT IMPLEMENTED
		
		# Alignment frequency
		self.a_mass            = dict()
		self._a_cache_mass_c   = dict()
		self._a_cache_mass_tot = 0.0
	
	#
	# Core methods
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
		self._set_alignment_mass(c1,c2,m+m*score)

		m = self._get_alignment_mass(c2,c1)
		self._set_alignment_mass(c2,c1,m+m*score)
		
	def discourage_alignment(self,c1,c2,score):
		"""
		TODO: update criterion according to reinforcement policy (operation +
		      simmetry)
		"""
		if c1.text == c2.text:
			return
		
		m = self._get_alignment_mass(c1,c2)
		
		m -= score

		self._set_alignment_mass(c1,c2,m)

	#
	# Input/Output methods
	#

	def import_ml(self,path):
		raise NotImplementedError

	def export_ml(self,path):
		"""
		Exports the Machine Learning data into human-readable files:
		   * path.ml.cfreq  - Chunk frequency data
		   * path.ml.ccfreq - Class-conditional chunk frequency data
		   * path.ml.afreq  - Alignment frequency data
		   
		NOTE: path includes the filename, but not the extension
		
		NOTE: the 'item' iterator is used in place of 'iteritems' to loop over
		      the dictionaries. This is to maintain the compatibility with 
		      Python3; on Python2 this causes the whole dictionary to be
		      replicated in the memory instead of be looped on the fly (as it
		      happens with 'iteritems' on py2 and with 'items' on py3), losing
		      efficiency.
		
		TODO: meta-symbols (TAB) are not escaped
		"""
		
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

		for k,v in self.c_mass.items():
			f_cfreq.write(k+u"\t"+unicode(v)+"\n")
		f_cfreq.write(u"\nT\t"+unicode(self._c_cache_mass_tot))
		f_cfreq.close()
		
		f_ccfreq.write(u"# This feature has not been implemented yet.")
		f_ccfreq.close()
		
		for k_i,v_i in self.a_mass.items():
			for k_j,v_j in v_i.items():
				f_afreq.write(k_i+u"\t"+k_j+u"\t"+unicode(v_j)+u"\n")
		f_afreq.write(u"\n")
		for k,v in self._a_cache_mass_c.items():
			f_afreq.write(u"T\t"+k+u"\t"+unicode(v)+u"\n")
		f_afreq.write(u"\nT\t"+unicode(self._a_cache_mass_tot))
		f_afreq.close()

	#
	# Private methods
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
		
		# Update alignment frequencies
		
		#~ if c1 > c2:
			#~ c1,c2 = c2,c1
		
		try:
			p_a_mass_c1 = self.a_mass[c1]
		except KeyError:
			p_a_mass_c1 = self.a_mass[c1] = dict()
			
			#~ assert c1 not in self._a_cache_mass_c ← can actually happen, because of the symmetry property
			self._a_cache_mass_c[c1] = self._a_cache_mass_c.get(c1,0)

		m_diff = m - p_a_mass_c1.get(c2,0)
		p_a_mass_c1[c2] = m
		
		# DEBUG
		import sys
		if self.a_mass[c1][c2] != m:
			sys.stderr.write(c1+","+c2+"\n")
			sys.stderr.write("a_mass = "+str(self.a_mass[c1][c2])+"\n")
			sys.stderr.write("m      = "+str(m)+"\n")
		assert self.a_mass[c1][c2] == m
		
		assert c1 in self._a_cache_mass_c
		self._a_cache_mass_c[c1] += m_diff

		#~ try:
			#~ self._a_cache_mass_c[c2] += m_diff
		#~ except KeyError:
			#~ assert m_diff == m
			#~ self._a_cache_mass_c[c2] = m_diff

		self._a_cache_mass_tot += m_diff
		
		# Increment the chunk counts
		
		try:
			self.c_mass[c1] += 1
		except KeyError:
			self.c_mass[c1] = 1

		try:
			self.c_mass[c2] += 1
		except KeyError:
			self.c_mass[c2] = 1
		
		self._c_cache_mass_tot += 2

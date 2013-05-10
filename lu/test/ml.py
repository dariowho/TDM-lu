# -*- coding: utf-8 -*-

"""
Test for the Machine Learning module
"""

from . import *
from lu import Chunk
from lu.ml.core import ML

what = "Machine Learning module"

_a = Chunk("first chunk",1)
_b = Chunk("second chunk",1)
_c = Chunk("three",1)
_d = Chunk("four",1)

def run():
	# Instantiation
	r = True
	try:
		ml = ML()
	except:
		r = False
	handle_test_result("Instantiation",r)
	
	# NewAl
	ml = ML()
	ml.reinforce_alignment(_a,_b,0.5)
		
	r = (ml._get_alignment_mass(_a,_b) == 0.5) and \
	    (ml._get_alignment_mass(_a) == ml._get_alignment_mass(_b) == 0.5) and \
	    (ml._get_alignment_mass() == 0.5)
	
	handle_test_result("NewAl",r)

	# DefaultAlMass
	ml = ML()
	r = ml._get_alignment_mass(_c,_d) == ml.DEFAULT_MASS
	
	handle_test_result("DefaultAlMass",r)

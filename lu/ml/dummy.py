# -*- coding: utf-8 -*-

"""
ML (dummy)
===============================================================================

This package is a dummy implementation of ML for debugging purposes

"""

import sys

PREFIX  = "[ML-dummy]: "

OUT_INIT         = True
OUT_GET_C_FREQ   = True
OUT_INC_C_FREQ   = True
OUT_GET_CC_FREQ  = True
OUT_INC_CC_FREQ  = True
OUT_GET_A_SCORE  = True
OUT_REINFORCE_A  = True
OUT_DISCOURAGE_A = True
OUT_IMPORT_ML    = True
OUT_EXPORT_ML    = True

def print_f(s):
	sys.stderr.write(PREFIX+s+"\n")

class ML(object):
	
	def __init__(self):
		if OUT_INIT:
			print_f("__init__")
	
	def get_c_frequency(self,c):
		if OUT_GET_C_FREQ:
			print_f("get_c_frequency("+c.text+")")
		
		return 0.0
	
	def increment_c_frequency(self,c):
		if OUT_INC_C_FREQ:
			print_f("increment_c_frequency("+c.text+")")
	
	def get_cc_frequency(self,c,m):
		if OUT_GET_CC_FREQ:
			print_f("get_cc_frequency("+c.text+","+m.label+")")
		
		return 0.0
	
	def increment_cc_frequency(self,c,m):
		if OUT_INC_CC_FREQ:
			print_f("increment_cc_frequency("+c.text+","+m.label+")")
	
	def get_alignment_score(self,c1,c2):
		if OUT_GET_A_SCORE:
			print_f("get_alignment_score("+c1.text+","+c2.text+")")
		
		return 0.0
	
	def reinforce_alignment(self,c1,c2,score):
		if OUT_REINFORCE_A:
			print_f("reinforce_alignment("+c1.text+","+c2.text+","+unicode(score)+")")
	
	def discourage_alignment(self,c1,c2,score):
		if OUT_DISCOURAGE_A:
			print_f("discourage_alignment("+c1.text+","+c2.text+","+unicode(score)+")")
			
	def import_ml(self,path,name):
		if OUT_IMPORT_ML:
			print_f("import_ml("+path+","+name+"):")
			
	def export_ml(self,path,name):
		if OUT_EXPORT_ML:
			print_f("export_ml("+path+","+name+"):")

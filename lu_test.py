#!/usr/bin/python2

"""
This script is a rudimental Regression Test Suite for the automated detection 
of bugs in the various components of the LU system.
"""

from lu.test import chunk,ml,summary

def run_test(module):
	print("Testing the "+module.what)
	print("==================================================================")
	module.run()
	print("")

run_test(chunk)
run_test(ml)

summary()

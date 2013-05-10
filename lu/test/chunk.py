# -*- coding: utf-8 -*-

"""
Test for the Chunk data structure
"""

from . import *
from lu import Chunk,Word

what = "Chunk data structure"

def run():
	# Equality
	a = Chunk("some text made of words",1)
	b = Chunk("some text made of words",1)
	r = (a == b)
	handle_test_result("Equality",r)

	# TextDifference
	a = Chunk("one two three",1)
	b = Chunk("four five six",1)
	r = (a != b)
	handle_test_result("TextDifference",r)

	# PosDifference
	a = Chunk("one two three",1)
	a = Chunk("one two three",2)
	r = (a != b)
	handle_test_result("PosDifference",r)

	# 123Words
	a = Chunk("one two three",1)
	r = a.words[0] == Word("one",1) and \
		a.words[1] == Word("two",2) and \
		a.words[2] == Word("three",3)
	handle_test_result("123Words",r)

	#SingletonEquality
	a = Chunk("oneword",1)
	b = Chunk("oneword",1)
	r = (a == b)
	handle_test_result("SingletonEquality",r)

	# SingletonTextDifference
	a = Chunk("oneword",1)
	b = Chunk("oneotherword",1)
	r = (a != b)
	handle_test_result("SingletonTextDifference",r)

	# SingletonPosDifference
	a = Chunk("sameword",1)
	a = Chunk("sameword",2)
	r = (a != b)
	handle_test_result("SingletonPosDifference",r)

	# SingletonWordEquality
	a = Chunk("one",1)
	b = Word("one",1)
	r = (a == b)
	handle_test_result("SingletonWordEquality",r)

	# SingletonWordTextDifference
	a = Chunk("oneword",1)
	b = Word("oneotherword",1)
	r = (a != b)
	handle_test_result("SingletonWordTextDifference",r)

	# SingletonPosDifference
	a = Chunk("sameword",1)
	a = Word("sameword",2)
	r = (a != b)
	handle_test_result("SingletonWordPosDifference",r)

	# Split
	a = Chunk("one two three four",1)
	[b,c] = a.split(2)
	b_t = Chunk("one two",1)
	c_t = Chunk("three four",3)
	r = (b==b_t) and (c==c_t)
	handle_test_result("Split",r)

	# SplitBegin
	a = Chunk("one two three four",1)
	[b,c] = a.split(1)
	b_t = Word("one",1)
	c_t = Chunk("two three four",2)
	r = (b==b_t) and (c==c_t)
	handle_test_result("SplitBegin",r)

	# SplitEnd
	a = Chunk("one two three four",1)
	[b,c] = a.split(3)
	b_t = Chunk("one two three",1)
	c_t = Word("four",4)
	r = (b==b_t) and (c==c_t)
	handle_test_result("SplitEnd",r)

	# SplitPos
	a = Chunk("one two three four",5)
	[b,c] = a.split(2)
	b_t = Chunk("one two",5)
	c_t = Chunk("three four",7)
	r = (b==b_t) and (c==c_t)
	handle_test_result("SplitPos",r)

	# SplitBeginPos
	a = Chunk("one two three four",5)
	[b,c] = a.split(1)
	b_t = Word("one",5)
	c_t = Chunk("two three four",6)
	r = (b==b_t) and (c==c_t)
	handle_test_result("SplitBeginPos",r)

	# SplitEndPos
	a = Chunk("one two three four",5)
	[b,c] = a.split(3)
	b_t = Chunk("one two three",5)
	c_t = Word("four",8)
	r = (b==b_t) and (c==c_t)
	handle_test_result("SplitEndPos",r)

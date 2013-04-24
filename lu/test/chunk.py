#!/usr/bin/python2

"""
Test for the Chunk data structure
"""

import sys

sys.path.append('..')
import LU

test_names   = []
test_results = []

def handle_test_result(name,result):
	print(name + ": "+unicode(result))
	test_names.append(name)
	if result == True:
		test_results.append(result)

def summary():
	print("--------------------------------------------")
	print(unicode(len(test_names))+" tests run; "+unicode(sum(test_results))+" passed.")
	
# Equality
a = LU.Chunk("some text made of words",1)
b = LU.Chunk("some text made of words",1)
r = (a == b)
handle_test_result("Equality",r)

# TextDifference
a = LU.Chunk("one two three",1)
b = LU.Chunk("four five six",1)
r = (a != b)
handle_test_result("TextDifference",r)

# PosDifference
a = LU.Chunk("one two three",1)
a = LU.Chunk("one two three",2)
r = (a != b)
handle_test_result("PosDifference",r)

# 123Words
a = LU.Chunk("one two three",1)
r = a.words[0] == LU.Word("one",1) and \
    a.words[1] == LU.Word("two",2) and \
    a.words[2] == LU.Word("three",3)
handle_test_result("123Words",r)

#SingletonEquality
a = LU.Chunk("oneword",1)
b = LU.Chunk("oneword",1)
r = (a == b)
handle_test_result("SingletonEquality",r)

# SingletonTextDifference
a = LU.Chunk("oneword",1)
b = LU.Chunk("oneotherword",1)
r = (a != b)
handle_test_result("SingletonTextDifference",r)

# SingletonPosDifference
a = LU.Chunk("sameword",1)
a = LU.Chunk("sameword",2)
r = (a != b)
handle_test_result("SingletonPosDifference",r)

# SingletonWordEquality
a = LU.Chunk("one",1)
b = LU.Word("one",1)
r = (a == b)
handle_test_result("SingletonWordEquality",r)

# SingletonWordTextDifference
a = LU.Chunk("oneword",1)
b = LU.Word("oneotherword",1)
r = (a != b)
handle_test_result("SingletonWordTextDifference",r)

# SingletonPosDifference
a = LU.Chunk("sameword",1)
a = LU.Word("sameword",2)
r = (a != b)
handle_test_result("SingletonWordPosDifference",r)

# Split
a = LU.Chunk("one two three four",1)
[b,c] = a.split(2)
b_t = LU.Chunk("one two",1)
c_t = LU.Chunk("three four",3)
r = (b==b_t) and (c==c_t)
handle_test_result("Split",r)

# SplitBegin
a = LU.Chunk("one two three four",1)
[b,c] = a.split(1)
b_t = LU.Word("one",1)
c_t = LU.Chunk("two three four",2)
r = (b==b_t) and (c==c_t)
handle_test_result("SplitBegin",r)

# SplitEnd
a = LU.Chunk("one two three four",1)
[b,c] = a.split(3)
b_t = LU.Chunk("one two three",1)
c_t = LU.Word("four",4)
r = (b==b_t) and (c==c_t)
handle_test_result("SplitEnd",r)

# SplitPos
a = LU.Chunk("one two three four",5)
[b,c] = a.split(2)
b_t = LU.Chunk("one two",5)
c_t = LU.Chunk("three four",7)
r = (b==b_t) and (c==c_t)
handle_test_result("SplitPos",r)

# SplitBeginPos
a = LU.Chunk("one two three four",5)
[b,c] = a.split(1)
b_t = LU.Word("one",5)
c_t = LU.Chunk("two three four",6)
r = (b==b_t) and (c==c_t)
handle_test_result("SplitBeginPos",r)

# SplitEndPos
a = LU.Chunk("one two three four",5)
[b,c] = a.split(3)
b_t = LU.Chunk("one two three",5)
c_t = LU.Word("four",8)
r = (b==b_t) and (c==c_t)
handle_test_result("SplitEndPos",r)



# SUMMARY
summary()

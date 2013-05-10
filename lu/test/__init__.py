# -*- coding: utf-8 -*-

#~ __all__ = ["chunk"]

test_names   = []
test_results = []

def handle_test_result(name,result):
	print(name + ": "+unicode(result))
	test_names.append(name)
	if result == True:
		test_results.append(result)

def summary():
	print("------------------------------------------------------------------")
	print(unicode(len(test_names))+" tests run; "+unicode(sum(test_results))+" passed.")

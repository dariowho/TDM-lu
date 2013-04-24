#!/usr/bin/python2

# http://nltk.googlecode.com/svn/trunk/doc/howto/wordnet.html

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wnic

brown_ic = wnic.ic('ic-brown.dat') 

def run(w1, w2):
	print (w1+" - "+w2+"(max; avg)")
	path_max = 0.0
	path_avg = 0.0
	path_n   = 0.0
	lch_max  = 0.0
	lch_avg  = 0.0
	lch_n    = 0.0
	wup_max  = 0.0
	wup_avg  = 0.0
	wup_n    = 0.0
	jcn_max  = 0.0
	jcn_avg  = 0.0
	jcn_n  = 0.0
	res_max  = 0.0
	res_avg  = 0.0
	res_n  = 0.0
	lin_max  = 0.0
	lin_avg  = 0.0
	lin_n  = 0.0
	for s1 in wn.synsets(w1, pos='v'):
		for s2 in wn.synsets(w2, pos='v'):
			path = s1.path_similarity(s2)
			if path > path_max:
				path_max = path
			if path is not None:
				path_avg = path_avg + path
				path_n = path_n + 1

			lch = s1.lch_similarity(s2)
			if lch > lch_max:
				lch_max = lch
			if lch is not None:
				lch_avg = lch_avg + lch
				lch_n = lch_n + 1
			
			wup = s1.wup_similarity(s2)
			if wup > wup_max:
				wup_max = wup
			if wup is not None:
				wup_avg = wup_avg + wup
				wup_n = wup_n + 1
			
			jcn = s1.jcn_similarity(s2,brown_ic)
			if jcn > jcn_max:
				jcn_max = jcn
			if jcn is not None:
				jcn_avg = jcn_avg + jcn
				jcn_n = jcn_n + 1
			
			res = s1.res_similarity(s2,brown_ic)
			if res > res_max:
				res_max = res
			if res is not None:
				res_avg = res_avg + res
				res_n = res_n + 1
			
			lin = s1.lin_similarity(s2,brown_ic)
			if lin > lin_max:
				lin_max = lin
			if lin is not None:
				lin_avg = lin_avg + lin
				lin_n = lin_n + 1
				
	print("\tPATH: "+str(path_max)+"; "+str(path_avg/path_n))
	print("\tLCH:  "+str(lch_max)+"; "+str(lch_avg/lch_n))
	print("\tWUP:  "+str(wup_max)+"; "+str(wup_avg/wup_n))
	print("\tJCN:  "+str(jcn_max)+"; "+str(jcn_avg/jcn_n))
	print("\tRES:  "+str(res_max)+"; "+str(res_avg/res_n))
	print("\tLIN:  "+str(lin_max)+"; "+str(lin_avg/lin_n))

run("increase","decrease")
run("increase","crank")
run("increase","pump")
run("increase","raise")
run("increase","lower")

run("decrease","shut")
run("decrease","up")
run("decrease","lower")
run("decrease","crank")
run("decrease","pump")
run("decrease","raise")


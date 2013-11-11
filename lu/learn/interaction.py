# -*- coding: utf-8 -*-

"""
Interaction - Learning interaction planning
===========================================

The purpose of this module is, given a learning situation, in which the system
is facing the task of classifying an unknown example, aiding the learning 
process by planning interactions with the user in case of necessity (i.e. when
the system is unable to classify the example with enough confidence).

An interaction plan consists of a sequence of questions leading to the disambi-
guation of the final meaning. These questions should help the system in the
association of the inner sentence constituents for the purpose of generalizing 
the learning experience to future cases.

NOTE: WIP

Constants
---------
   ALPHA Maximum confidence bound: if a meaning covers a score portion greater
         than ALPHA, this meaning is automatically selected as final.
   BETA  Minimum confidence bound: if none of the meaning covers a score por-
         tion greater than BETA the system shall ask the user to rephrase. If
         some meanings are greater than BETA, but none of them is greater than
         ALPHA, the system shall try to disambiguate between these meanings.
   
   
Error codes
-----------
   E_PARBOUND   Parameters should not be greater or equal than 1
   E_SMALLALPHA ALPHA should be greater than 0.5 (if a meaning achieves a score
                bigger than ALPHA, that meaning should be the only one)
   E_BIGBETA    BETA should be smaller than 0.5 (It sould be possible for two
                meanings to lay in the region between BETA and ALPHA)
"""

import pdb

from lu.score.word import WordScore

ALPHA = 0.7
BETA  = 0.3

GAMMA = 0.5

E_PARBOUND   = 1
E_SMALLALPHA = 2
E_BIGBETA    = 3

PREFIX = "[LU.learn.interaction] "

tdm_ground_stack = []	# This is just for hacked TDM interaction

def get_plan(u):
	"""
	Given a candidate output of Language.understand(), makes a decision wether
	the understanding needs the intervention of the user for disambiguation. If
	yes, returns a set of questions to ask, which results can aid the learning
	process.
	
	NOTE: WIP
	
	TODO: replace array positions with constants
	"""
	
	if u[0][1] > ALPHA:
		print (PREFIX+"get_plan(): "+u[0][0]+" accepted with top confidence")
		return [ u[0] ]

	if u[0][1] > BETA:
		l = []
		for m in u:
			if m[1] > BETA:
				l.append(m)
				
		if (len(l)==1):
			print(PREFIX+"get_plan(): "+l[0][0]+" accepted with low confidence")
		else:
			print(PREFIX+"get_plan(): disambiguating between "+unicode(l[0]))

		print(PREFIX+"get_plan(): questions: "+ unicode(get_questions(l)) )
		
		return l
	
	print (PREFIX+"get_plan(): no meaning has enough confidence: rephrase")
	return []

def get_plan_tdm(u):
	"""
	Get an OpenTDM compatible plan.
	
	NOTE: This function is specific for thesis, and very likely not to be 
	      useful in a general-purpose library.
	
	INPUT
	   'u' is a list of tuples (meaning_label, score_float, score), output of
	       Language.understand()
	
	OUTPUT
		A list of tuples (meaning_label, score_float, score, questions) that 
		can be interpreted by OpenTDM to perform the move, ground a move, 
		disambiguate between multiple meanings or ask to rephrase; 'questions'
		is a list of natural language questions that are meant to be asked.
		
		As a side-effect, every time a grounding issue is generated, this is 
		pushed in a stack of open grounding issues. This stack will be used to
		handle future yes/no user answers.
		Note that this is a thesis-purposes hack to make things work in TDM,
		should be removed in any stable version of the library.
	"""

	u_plan = get_plan(u)
	
	if len(u_plan) == 0:
		"""No possible interpretations: rephrase"""
		return [ [ 'request(_rephrase)', 1.0, None, [] ] ]
	
	if len(u_plan) == 1:
		"""One possible interpretation"""
		if u_plan[0][1] > ALPHA:
			"""Perform"""
			u_plan[0].append([])
			return u_plan
		else:
			"""Ground"""
			questions = get_questions(u_plan)
			tdm_ground_stack.append([u_plan[0][0],\
			                         u_plan[0][2].meaning,\
			                         u_plan[0][2].sentence])
			return [ [ 'request(_ground)', 1.0, None, questions ] ]
	
	"""Multiple interpretations: disambiguate"""
	# TODO: change with appropriate disambiguation action (at the moment 
	#       this is dealt with as in the single-sentence grounding)
	questions = get_questions([ u_plan[0] ])
	tdm_ground_stack.append([u_plan[0][0],\
						     u_plan[0][2].meaning,\
						     u_plan[0][2].sentence])
	return [ [ 'request(_ground)', 1.0, None, questions ] ]



def get_questions(understanding_list):
	"""
	WIP
	"""
	
	if (len(understanding_list)==1):
		return _get_questions_chunk(understanding_list[0][2].max_sscore_full)
	else:
		r = []
		for m in understanding_list:
			l = ["Does "+unicode(m[2].sentence)+" mean "+\
			     unicode(m[2].max_sscore_full.s_to)+"?"]
			l.append(_get_questions_chunk(m[2].max_sscore_full))
			r.append(l)
		return r

def validate_constants():
	"""
	Returns 0 if the module's constants are set to acceptable values, an error
	code >0 otherwise.
	"""
	
	if (ALPHA >= 1) or (BETA >=1):
		return E_PARBOUND

	if (ALPHA <= 0.5):
		return E_SMALLALPHA
	
	if (BETA > 0.5):
		return E_BIGBETA
		
	return 0


def _get_questions_chunk(s):
	"""
	Recursively determine which questions to ask about a sentence match, which 
	is represented by the input Score s. s is meant to be either a ChunkScore
	or a WordScore
	
	NOTE: WIP
	
	NOTE: The function is mean to return a list of (maybe nested) questions.
	      However at the moment the list will contain only one element. This
	      is meant to be improved in the future.
	"""
	
	if type(s)==WordScore:
		return (["Does "+unicode(s.s_from)+" mean "+unicode(s.s_to)+"?"])
	
	r = []
	
	# TODO: There might be only one chunk in s (is this even true?)
	
	s1 = s.alignment[0].get_score()
	s2 = s.alignment[1].get_score()
	_sum = s1+s2
	s1 = s1/_sum
	s2 = s2/_sum
	
	if (s1-s2 > GAMMA):
		if (s1<s2):
			return _get_questions_chunk(s.alignment[0])
		else:
			return _get_questions_chunk(s.alignment[1])
	else:
		r.append(["Does "+unicode(s.s_from)+" mean "+unicode(s.s_to)+"?"])
		         
	return r

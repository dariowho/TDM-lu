# -*- coding: utf-8 -*-

"""
This module contains code for rendering a MeaningScore object into a human-
readable file format.

At the moment only the HTML format is available.
"""

import lu.score.output.m2table

_html_prefix = 0

def render_html(ms):
	"""
	Renders a MeaningScore object (ms) into HTML code
	"""
	
	global _html_prefix
	
	print("<h1>Meaning: "+unicode(ms.meaning)+"</h1>")
	print("<ul class='score'>")
	print(unicode(ms.meaning)+"<br/>")
	print(unicode(ms.sentence))
	for f in ms.features:
		print("<li>"+unicode(f)+"</li>")
	print("<li class='total'>"+str(ms.get_score())+"</li>")
	print("</ul>")
	
	print("<ul>")
	# NOTE: as of now, a sentence score, ss, is just a ChunkScore
	for ss in ms.s_sscores:
		prefix = str(_html_prefix)+"-"
		lu.score.output.m2table.render_html(ss.s_table,None,prefix)
		_html_prefix = _html_prefix+1
	print("</ul>")

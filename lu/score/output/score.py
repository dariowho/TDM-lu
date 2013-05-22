# -*- coding: utf-8 -*-

"""
This module contains code for rendering a MeaningScore object into a human-
readable file format.

At the moment only the HTML format is available.
"""

def render_html(s):
	"""
	Renders a Score object (s) into HTML code
	"""
	
	print("<ul class='score'>")
	print(s.s_from_tree.penn_string()+"<br/>")
	print(s.s_to_tree.penn_string())
	for f in s.features:
		print("<li>"+unicode(f)+"</li>")
	print("<li class='total'>"+unicode(s.get_score())+"</li>")
	print("</ul>")

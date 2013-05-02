# -*- coding: utf-8 -*-

"""
This module contains code for rendering a M2Table object into a human-
readable file format.

At the moment only TXT and HTML formats are supported.
"""

import lu.score.output.score

def render_txt(table,from_a=1,from_b=None,indent=0):
	"""
	Outputs a M2Table in text format.
	
	TODO: this function has not been tested since it was moved from score.chunk
	"""
	if from_b == None:
		from_b = table.chunk_from.length
		
	assert from_a > 0
	assert from_a <= table.chunk_from.length
	assert from_b > 0
	assert from_b <= table.chunk_from.length
	assert from_a <= from_b
	
	if from_a == from_b:
		print("\t"*indent+"-"+str(from_a)+"-,-"+str(from_b)+"-")
		return
	
	for i in range(from_a,from_b):
		print("\t"*indent+"("+str(from_a)+","+str(i)+","+str(from_b)+")")
		render_txt(table,from_a,i,indent+1)
		render_txt(table,i+1,from_b,indent+1)


def render_html(table,chunk=None,prefix="",indent=0):
	"""
	Outputs a M2Table in HTML format
	"""
	if chunk == None:
		chunk = table.chunk_from
		_render_html_sd_all(table,chunk,prefix,indent)

	chunk_start = chunk.position
	chunk_end   = chunk.position+chunk.length-1
	sd_id       = "sd-"+prefix+str(chunk_start)+"-"+str(chunk_end)
		
	print("\t"*indent+"<li><a href='#' onmouseover='showSD(\""+sd_id+"\")'>"+str(chunk)+" - <span class='light'>"+str(table.chunk_to)+"</span></a>")
	if not chunk.is_word():
		print("\t"*indent+"<ul>")
		for i in range(1,chunk.length):
			cc = chunk.split(i)
			print("\t"*indent+"<li><a href='#'>"+" | ".join([str(x) for x in cc])+" - <span class='light'>"+str(table.chunk_to)+"</span></a>")
			print("\t"*indent+"<ul>")
			for c in cc:
				render_html(table,c,prefix,indent+1)
			print("\t"*indent+"</ul>")
			print("\t"*indent+"</li>")
		print("\t"*indent+"</ul>")
	print("\t"*indent+"</li>")
	print("")

def _render_html_sd_all(table,chunk,prefix,indent,donelist=[]):
	chunk_start = chunk.position
	chunk_end   = chunk.position+chunk.length-1
	sd_id = "sd-"+prefix+str(chunk_start)+"-"+str(chunk_end)
	if sd_id not in donelist:
		_render_html_sd(table,chunk,sd_id,indent)

	if not chunk.is_word():
		for i in range(1,chunk.length):
			cc = chunk.split(i)
			for c in cc:
				_render_html_sd_all(table,c,prefix,indent,donelist)


def _render_html_sd(table,chunk,sd_id,indent):
	print("\t"*indent+"<div class='sd' id='"+sd_id+"'>")
	print("\t"*indent+"<p>All the possible scores of <em>"+chunk.text+"</em>.</p>")
	print("\t"*indent+"<ul>")
	_render_html_sd_inner(table,chunk,None,indent)
	print("\t"*indent+"</ul>")
	print("\t"*indent+"</div>")
	
def _render_html_sd_inner(table,chunk_from,chunk_to=None,indent=0):
	if chunk_to is None:
		chunk_to = table.chunk_to

	print("\t"*indent+"<li>")
	print("\t"*indent+"<a href='#'><span class='light'>"+str(chunk_from)+"</span> - "+str(chunk_to)+"</a>")
	score = table.get_score(chunk_from,chunk_to)
	lu.score.output.score.render_html(score)
	if not chunk_to.is_word():
		print("\t"*indent+"<ul>")
		for i in range(1,chunk_to.length):
			cc = chunk_to.split(i)
			print("\t"*indent+"<li><a href='#'><span class='light'>"+str(chunk_from)+"</span> - "+" | ".join([str(x) for x in cc])+"</a>")
			print("\t"*indent+"<ul>")
			for c in cc:
				_render_html_sd_inner(table,chunk_from,c,indent+1)
			print("\t"*indent+"</ul>")
			print("\t"*indent+"</li>")
		print("\t"*indent+"</ul>")
	print("\t"*indent+"</li>")

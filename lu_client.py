#!/usr/bin/python2

"""
This script is a sample client for the Language Unit
"""

from lu import LU
import lu.ml


l = LU.Language()

#
# ML I/O DEBUG
#

#~ LANGUAGE_NAME = "stub_language_m2"
#~ l.import_l("lu/language_base/",LANGUAGE_NAME)
#~ 
#~ lu.ml.export_ml("lu/_out/",LANGUAGE_NAME+"_ex1")
#~ print(str(lu.ml.ml_data_exist("lu/_out/",LANGUAGE_NAME+"_ex1")))
#~ print(str(lu.ml.ml_data_exist("lu/_out/",LANGUAGE_NAME+"_ex2")))
#~ lu.ml.import_ml("lu/_out/",LANGUAGE_NAME+"_ex1")
#~ lu.ml.export_ml("lu/_out/",LANGUAGE_NAME+"_ex2")

#
# LEARN DEBUG
#

#~ """
#~ Use the ML-dummy module, replacing in ml/__init.__py "from ml.core import ML"
#~ with "from ml.dummy import ML"
#~ """
#~ 
#~ LANGUAGE_NAME = "toy"
#~ l.import_l("lu/language_base/",LANGUAGE_NAME)
#~ 
#~ l.learn("one two three","1")


#
# M2 DEBUG
#

LANGUAGE_NAME = "stub_language"
l.import_l("lu/language_base/",LANGUAGE_NAME)

print("<!DOCTYPE html>\n\
<html>\n\
<head>\n\
  <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">\n\
  <title>LU Output debugger</title>\n\
  \n\
  <script type='text/javascript' src='jquery-1.9.1.min.js'></script>\n\
  \n\
  <link rel=\"stylesheet\" type=\"text/css\" href=\"lu_client.out.css\"> \
\n\
\n\
<script type='text/javascript'>\n\
function showSD(id) {\n\
  $('.sd').hide();\n\
  $('#'+id).show(); \n\
}\n\
\n\
//<![CDATA[ \n\
$(window).load(function(){\n\
$(\"#content li > a\").click(function() {\n\
    var li = $(this).closest('li');\n\
    li.find(' > ul').slideToggle('fast');\n\
});\n\
});\n\
\n\
//]]>  \n\
\n\
</script>\n\
\n\
\n\
</head>\n\
<body>\n\
	<p onclick=\"showSD('sd-default');\" class=\"maintitle\">LU "+LU.__version__+"</p>\n\
	\n\
  <div id=\"content\">\n\
  	<div class=\"sd\" id=\"sd-default\">\
		<p>Click on a score to display its detail</p>\
	</div>\
	<div id=\"left\">")


#~ l.understand_debug("increase the volume please")
l.understand_debug("turn up the volume")

print("	</div>\
<script>\
showSD('sd-default');\
</script>\
</body>\
\
\
</html>")


#
# BASE
#

#~ LANGUAGE_NAME = "stub_language"
#~ l.import_l("lu/language_base/",LANGUAGE_NAME)
#~ 
#~ # l.export_l("language_base/stub_language_E.l")
#~ 
#~ l.understand_debug("increase the volume, please")


#~ lu.ml.export_ml("lu/_out/",LANGUAGE_NAME)

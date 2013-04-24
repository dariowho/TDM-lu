#!/usr/bin/python2

from lu import LU

l = LU.Language()

l.import_l("lu/language_base/stub_language_m2.l")


# M2 DEBUG


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


l.understand("increase the volume please")

print("	</div>\
<script>\
showSD('sd-default');\
</script>\
</body>\
\
\
</html>")


#~ # BASE
#~ 
#~ # l.export_l("language_base/stub_language_E.l")
#~ 
#~ l.understand("increase the volume, please")

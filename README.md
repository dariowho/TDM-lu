TDM-lu
======

The Language Unit is a Natural Language Understanding module, meant to serve as a replacement for the Grammatical Framework in TRINDI-kit-based Dialogue Managers (early developement stage!)

System requirements
===================

The code requires Python 2.7 (http://www.python.org/download/releases/2.7/) and the NLTK (http://nltk.org/)


Running the code
================

A test client (lu_client.py) is provided. It can be run with:

```
python2 lu_client.py > lu_client.out.html 
```

The script produces an HTML file containing the detail of a sentence scored against all the meanings in a grammar.

from nltk import tokenize

#
# Data Structures
#

class Meaning(object):
	"""
	A Meaning in the Language is defined by a list of representative sentences
	expressing it.
	
	TODO: define other properties of Meanings, eg. a prior on their probability
	      given by the relative count of uses
	"""

	def __init__(self,label_in,sentences_in = None,frequencies_in = None):
		"""
		A Meaning is initialized with the list of its sentences and their 
		frequencies. The frequency of a sentence can be give, for example, by
		the number of times it was used in the application.
		
		TODO: can the same Sentence appear in more than one meaning?
		TODO: include other parameters, eg. the confidency degree of a sentence
		      belonging to this meaning (1 if present in the grammar, $SCORE if
		      guessed by the LU, + reinforcement etc.)
		"""
		assert (sentences_in == None and frequencies_in == None) or \
		       (sentences_in != None and frequencies_in != None)
		
		if sentences_in == None:
			sentences_in = []
			frequencies_in = []
		
		assert len(sentences_in) == len(frequencies_in)
		
		self.label       = label_in
		self.sentences   = sentences_in
		self.frequencies = frequencies_in

	def add_sentence(self,sentence_in,frequence_in):
		self.sentences.append(sentence_in)
		self.frequencies.append(frequence_in)

	def __str__(self):
		return "m'"+self.label+"'"
		
	def __repr__(self):
		return self.__str__()

class Chunk(object):
	"""
	A Chunk is a piece of sentence containing one or more words. It is ini-
	tialised with it text content and its position in the sentence (number 
	of Chunks preceding it, plus one).
	
	Even though this is meant to be done only by Chunk methods, a Chunk can be
	initialized with a list of words. In this case no text content is expected.
	
	The text content is always set by concatenating the single words with
	spaces. NOTE: the text content may differ from the initialization string
	(eg. "One, two, three" > "One , two , three") 
	"""
	
	# The function which is used to tokenize input: it is important that chunks
	# of text are always tokenized the same way
	_tokenize = tokenize.WordPunctTokenizer().tokenize
	
	def __init__(self,text_in,position_in,_words_in=None):
		assert position_in > 0
		assert (text_in is not None) ^ (_words_in is not None)
		
		# Words list can be given or extracted from the text input string
		if _words_in is not None:
			self.words = _words_in
		else:
			self.words = [Word(x,position_in+i) for i,x in enumerate(Chunk._tokenize(text_in))]

		self.position  = position_in
		self.text  = " ".join([x.text for x in self.words])
		self.length    = len(self.words)

	def __eq__(self,other):
		if other is None:
			return False
		
		if self.length == 1 and other.length == 1:
			return (self.text == other.text) and (self.position == other.position)
		
		return (self.words == other.words) and (self.position == other.position)
	
	def __ne__(self,other):
		return not self.__eq__(other)
		
	def is_word(self):
		return self.length == 1
	
	def split(self,n):
		"""
		Split the chunk in two smaller chunks, the first from the beginning to 
		the n-th word (included) and the second from the [n+1]-th word to the 
		end.
		
		Returns a list containing the two chunks, or a single chunk being self
		is the split is on the last word.
		
		Single word chunks are always returned as Word objects.
		"""
		assert n <= self.length
		assert n >= 1
		
		if n == 1:
			if n == self.length:
				assert len(self.words) == 1
				return ChunkedChunk(self.words)
				
			c1 = self.words[0]
		else:
			if n == self.length:
				return ChunkedChunk([self])
				
			c1 = Chunk(None,self.position,self.words[:n])
		
		c2 = Chunk(None,self.position+n,self.words[n:])
		
		return ChunkedChunk([c1,c2])
	
	def penn_string(self):
		return "c'"+self.text+"'"
		
	def __str__(self):
		return self.penn_string()
		
	def __repr__(self):
		return self.__str__()

class ChunkedChunk(list):
	"""
	How much wood would a woodchuck chunk if a woodchuk could chunk wood?
	
	TODO: test this data structure
	TODO: check the efficiency of the text field: might be recursively expensive,
	      and it's used only to keep the consistency of merge (which is used only
	      for a temp. feature of M2)
	"""
	
	def __init__(self, *args):
		list.__init__(self, *args)
		self.length = 0
		for c in self:
			self.length = self.length + c.length
		self.text = ' '.join([x.text for x in self])
	
	def is_word(self):
		return (len(self)==1) and (self[0].is_word())
	
	def merge(self):
		"""
		TODO: This is very temporary
		"""
		
		return Chunk(self.text,self[0].position)
	
	def penn_string(self):
		"""
		Return the chunk as a string in the Penn Treebank format
		"""
		
		#~ return "(CC "+" ".join(x.penn_string() for x in self)+")"
		return "(CC "+" ".join(str(x) for x in self)+")"
		
	def __str__(self):
		return self.penn_string()
		
	def __repr__(self):
		return self.__str__()
		

class Word(object):
	"""
	A Word is a Chunk with one word.
	
	TODO: consider removing this class, because it doesn't add anything to a 
	      one-word chunk, replicate all of its methods, and in the code it is 
	      used together with one-word chunks
	"""
	
	def __init__(self,text_in,position_in):
		
		self.text     = text_in
		self.position = position_in
		self.length   = 1
	
	def __eq__(self,other):
		if other is None:
			return False
		
		return (self.text == other.text) and (self.position == other.position)
	
	def __ne__(self,other):
		return not self.__eq__(other)
		
	def __str__(self):
		return self.text+str(self.position)
		
	def __repr__(self):
		return self.__str__()

	def is_word(self):
		return True
	
	def split(self,n):
		assert n == 1
		
		return ChunkedChunk([self])
		
	def penn_string(self):
		return "w'"+self.text+"'"


class Sentence(Chunk):
	"""
	A Sentence is a Chunk that denotes at least one meaning.
	
	TODO: thing about some properties for a sentence, eg. uses count
	"""
	
	def __init__(self,text_in):
		super(Sentence,self).__init__(text_in,1)
	
	def is_sentence(self):
		return True

	def __str__(self):
		return "s'"+self.text+"'"
		
	def __repr__(self):
		return self.__str__()

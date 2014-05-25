import re
#import vim

def displaysearch(search):
	if search is None:
		return None
	return '<Search: %r, groups=%r>' % (search.group(), search.groups())

class Scope:
	def __init__(self, name, list_key_start, list_scope_child, list_key_end):
		self.name = name
		self.list_key_start = list_key_start
		self.list_scope_child = list_scope_child
		self.list_key_end = list_key_end


class Key:
	def __init__(self, name, string_pattern, ):
		self.name = name
		self.string_pattern = string_pattern
		self.pattern = re.compile(string_pattern)
		
	def test(self, word):
		if self.pattern.match(word):
			return True

		return False

scope_none = Scope(
	'none',
	[],
	['preproc if','preproc ifndef'],
	[]);

scope_class = Scope(
	'class',
	['class'],
	['class body'],
	[('semicolon',True)])

scope_class_body = Scope(
	'class body',
	['curly open'],
	[],
	[('curly close',True)])

scope_preproc_if = Scope(
	'preproc if',	
	['preproc if'],
	['class'],
	[('preproc endif',True)])


scope_preproc_ifndef = Scope(
	'preproc ifndef',
	['preproc ifndef'],
	['class'],
	[])


list_scope = {
	'class':		scope_class,
	'class body':		scope_class_body,
	'preproc define':	Scope('preproc define',[],[],[]),
	'preproc if':		scope_preproc_if,
	'preproc ifndef':	scope_preproc_ifndef,
	'preproc else':		Scope('preproc else',[],[],[]),
	'preproc elif':		Scope('preproc elif',[],[],[]),
	'preproc endif':	Scope('preproc endif',[],[],[])}




key_class = Key(
	'class',
	'class$')

key_semicolon = Key(
	'semicolon',
	';')

key_preproc_if = Key(
	'preproc if',	
	'#if$')

key_preproc_ifndef = Key(
	'preproc ifndef',
	'#ifndef$')

list_key = {
	'class':		key_class,
	'curly open':		Key('curly open','{$'),
	'curly close':		Key('curly open','}$'),
	'semicolon':		key_semicolon,
	'preproc define':	Key('preproc define','#define$'),
	'preproc if':		key_preproc_if,
	'preproc ifndef':	key_preproc_ifndef,
	'preproc else':		Key('preproc else','#else$'),
	'preproc elif':		Key('preproc elif','#elif$'),
	'preproc endif':	Key('preproc endif','#endif$')}
	
def key_in_scope_start(key, list_scope_):
	for scope_name in list_scope_:
		scope = list_scope[scope_name]
		if key in scope.list_key_start:
			return scope
	
	return None


class Chunk:
	def __init__(self, words, scope=scope_none):
		self.words = words
		self.keep = []
		self.scope = scope
		
#	def scan_start(self):
#		ret = []
#		if self.scope.list_key_start:
#			while self.words:
#				w = self.words.pop(0)
#				
#				k = classify(w)
#				
#				# terminator
#				if k in self.scope.list_key_start:
#					self.keep.append(w)
#					return ret
#				
#				# discard
#				#if any(w == s for s in discard):
#				#	continue
#				# neutral
#				self.keep.append(w)

	def process(self):
		#term = terminator_dict[self.code]
		
		# if chunk has a starter, then it was created by another call to process and we should therefore scan for an initiator
		#self.scan_start()
		
		#print self.words
		
		# do until all words are poped
		while self.words:
			# pop words until starter is found
			word = self.words.pop(0)
			#print "%r" % word
			
			
			key = classify(word)
			#print "key={0}".format(key)
			#print "end={0}".format(self.scope.list_key_end)
			
			# child
			scope = key_in_scope_start(key, self.scope.list_scope_child)
			if scope:
				# create new chunk
				new_chunk = Chunk(self.words, scope)
				
				new_chunk.keep.append(word)

				print "word"
				print word
				print "words"
				print self.words
				print "keep"
				print self.keep
				print new_chunk.keep

				self.words = new_chunk.process()
											
				self.keep.append(new_chunk)
					
				continue
			
			# end
			for k,b in self.scope.list_key_end: #if term != 0:
				if key == k:
					
					# immediate terminator
					#if term == 1:
					#	ret = self.words
					#	ret.insert(0,word)
					#	self.words = []
					#	return ret
					# return what was not used
					#if word == term:
	
					# keep or return the end word?
					if b:
						self.keep.append(word)
					else:
						self.words.insert(0,word)
					
					# return all unused words
					ret = self.words
					self.words = []
					
					return ret
			
			# if word is neither a start nor an end, keep it
			self.keep.append(word)
			
		return []

	def cprint(self,prefix=''):
		#print self.keep

		keep = self.keep
		
		string = ''
		
		while keep:
			word = keep.pop(0)
			
			
			if isinstance(word,Chunk):
				if string != '':
					print prefix+string
					string = ''
				
				word.cprint(prefix+'\t')
			elif word == '\n':
				if string != '':
					print prefix+string
					string = ''

			else:
				string += word
		
		
		if string != '':
			print prefix+string
			string = ''
	
				


def classify(word):
	for k,v in list_key.items():
		if v.test(word):
			#print "'{0}' is a '{1}' key".format(word,v.name)
			return k

	return None

def get_buffer():
	word_list = []

	cb = vim.current.buffer
	
	for i in range(0,len(cb)):
		line = cb[i]
		#print line
		word_list.append(line+'\n')
	
	return word_list

def fragment(list_word, string_pattern):
	pat = re.compile(string_pattern)
	
	list_word_frag = []
	
	for word in list_word:
		list_subword = pat.split(word)
		#for subword in list_subword:
		#	list_word_frag.append(subword)
		list_word_frag += list_subword
		
	return list_word_frag
	
def nullstring(x):
	if x == '':
		return False
	return True
	
def reformat():
	list_word = get_buffer();
	#print list_word
	
	list_word = fragment(list_word, "[\t\ ]+")
	#print list_word
	
	list_word = fragment(list_word, "([\n{};])")
	#print list_word
	
	list_word = filter(nullstring,list_word)
	print list_word

	
	# global chunk
	gchunk = Chunk(list_word)
	gchunk.process()
	
	
	#print_chunk(gchunk,"",0)
	print '%%%'
	gchunk.cprint()
	
	print '%%%'
	print gchunk.keep


if __name__ == '__main__':
	with open('test.h','r') as f:
		lines = f.readlines()
	
	gchunk = Chunk(lines)
	gchunk.process()

	print gchunk.keep
	print gchunk.scope


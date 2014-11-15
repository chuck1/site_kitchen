#!/usr/bin/env python
#
import re
#import vim

def displaysearch(search):
	if search is None:
		return None
	return '<Search: %r, groups=%r>' % (search.group(), search.groups())

class Scope:
	def __init__(self, name, list_key_start, list_scope_child, list_key_end):
                #print 'scope __init__'
		self.name = name
		self.list_key_start = list_key_start

                # possible child scopes
                self.list_scope_child = list_scope_child

		self.list_key_end = list_key_end


class Key:
	def __init__(self, name, string_pattern, ):
                #print 'Key __init__'
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
	['preproc if','preproc ifndef','preproc include','function'],
	[]);

# class
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

# ns
scope_ns = Scope(
	'ns',
	['ns'],
	['ns body'],
	[('curly close',True)])

# list_key_end:
#     pass curly close back to 'ns' to close 'ns'
scope_ns_body = Scope(
	'ns body',
	['curly open'],
	['ns','class'],
	[('curly close',False)])


# preproc

scope_preproc_if = Scope(
	'preproc if',	
	['preproc if'],
	['class','ns'],
	[('preproc endif',True)])


scope_preproc_ifndef = Scope(
	'preproc ifndef',
	['preproc ifndef'],
	['class','ns'],
	[])


list_scope = {
	'class':		scope_class,
	'class body':		scope_class_body,
	'ns':	        	scope_ns,
	'ns body':		scope_ns_body,
	'preproc define':	Scope('preproc define',[],[],[]),
	'preproc if':		scope_preproc_if,
	'preproc ifndef':	scope_preproc_ifndef,
	'preproc include':	Scope('preproc include',['preproc include'],[],[('newline',True)]),
	'preproc else':		Scope('preproc else',[],[],[]),
	'preproc elif':		Scope('preproc elif',[],[],[]),
	'preproc endif':	Scope('preproc endif',[],[],[]),
        'function':             Scope('function',['word'],['function body','function params'],[('curly close',True)]),
        'function body':        Scope('function body',['curly open'],[],[('curly close',False)]),
        'function params':      Scope('function params',['paren open'],[],[('paren close',True)])
        }




key_class = Key(
	'class',
	'class$')

key_ns = Key(
	'namespace',
	'namespace$')

key_semicolon = Key(
	'semicolon',
	';')

key_preproc_if = Key(
	'preproc if',	
	'#if$')

key_preproc_ifndef = Key(
	'preproc ifndef',
	'#ifndef$')

key_preproc_include = Key(
	'preproc include',
	'#include$')

list_key = {
        'newline':              Key('newline','^\n$'),
        'class':		key_class,
        'ns':                   key_ns,
	'curly open':		Key('curly open','{$'),
	'curly close':		Key('curly close','}$'),
	'paren open':		Key('paren open','\($'),
	'paren close':		Key('paren close','\)$'),
	'semicolon':		key_semicolon,
	'preproc define':	Key('preproc define','#define$'),
	'preproc if':		key_preproc_if,
	'preproc ifndef':	key_preproc_ifndef,
	'preproc include':	key_preproc_include,
	'preproc else':		Key('preproc else','#else$'),
	'preproc elif':		Key('preproc elif','#elif$'),
	'preproc endif':	Key('preproc endif','#endif$'),
        'word':                 Key('word','\w+')
        }


def key_in_scope_start(key, list_scope_):
        #print 'key_in_scope_start'
        #print '    key =',repr(key)
        #print '    list_scope_ =',list_scope_

	for scope_name in list_scope_:
		scope = list_scope[scope_name]
		if key in scope.list_key_start:
                    #print 'returning',scope
		    return scope
	
	return None



class Chunk:
	def __init__(self, parent, words, scope=scope_none):

                #print 'words:'
                #for w in words:
                #    print '   ',repr(w)

                self.parent = parent
                self.words = words
		self.keep = []
		self.scope = scope

	def __str__(self):
		return self.__class__.__name__+" "+self.scope.name

        def printvar(self,prefix=''):
            #print 'words:'
            #print self.words

            #if self.scope:
            #    print prefix+'scope:', self.scope.name
            #else:
            #    print prefix+'scope:', self.scope

            #print prefix+'keep:'

            temp = []

            for k in self.keep:
                if isinstance(k,Chunk):

                    if temp:
                        print prefix + repr(" ".join(temp))
                        temp = []

                    print prefix+str(k)
                    k.printvar(prefix+'\t')
                else:
                    if k != '\n':
	                    #print prefix + repr(k)
                            temp.append(k)

            if temp:
                print prefix + repr(" ".join(temp))

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


        def gen_chunks(self):
            for k in self.keep:
                if isinstance(k,Chunk):
                    yield k

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
	
class Namespace(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

        def name(self):
            return self.keep[1]

class NamespaceBody(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

class Class(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

        def name(self):
            return self.keep[1]

class ClassBody(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

class PreProc(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

class Function(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__ + " " + self.name()
	def name(self):
		s = re.split('::', self.keep[0])
		return str(s)
		return self.keep[0]

class FunctionBody(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

class FunctionParams(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__

class ChunkNone(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return self.__class__.__name__



## generators

def gen_namespace(c):
    for l in c.keep:
        if isinstance(l, Namespace):
            yield l
        elif isinstance(l, PreProc):
            for l2 in gen_namespace(l):
                yield l2

def gen_class(c):
    for l in c.keep:
        if isinstance(l, Class):
            yield l
        elif isinstance(l, PreProc):
            for l2 in gen_class(l):
                yield l2
        elif isinstance(l, NamespaceBody):
            for l2 in gen_class(l):
                yield l2

def gen_full(c):
    for cl in gen_class(c):
        yield [cl.name()]
    
    for ns in gen_namespace(c):
        for s in gen_full(ns):
            yield [ns.name()] + s


# main process function

def process(c):
	#term = terminator_dict[c.code]
	
	# if chunk has a starter, then it was created by another call to process and we should therefore scan for an initiator
	#c.scan_start()
	
	#print c.words
	
	# do until all words are poped
	while c.words:
		# pop words until starter is found
		word = c.words.pop(0)
		#print "%r" % word
		

		key = classify(word)
		#print "key={0}".format(key)
		#print "end={0}".format(c.scope.list_key_end)

                        #print '    word =',repr(word)
		#print '    key =',repr(key)
		
		# child
		scope = key_in_scope_start(key, c.scope.list_scope_child)
		if scope:
                        #print "creating chunk",scope.name
			# create new chunk
                        if scope.name == 'ns':
                            new_chunk = Namespace(c, c.words, scope)
                        elif scope.name == 'ns body':
                            new_chunk = NamespaceBody(c, c.words, scope)
                        elif scope.name == 'class':
                            new_chunk = Class(c, c.words, scope)
                        elif scope.name == 'class body':
                            new_chunk = ClassBody(c, c.words, scope)
                        elif scope.name == 'preproc ifndef':
                            new_chunk = PreProc(c, c.words, scope)
                        elif scope.name == 'function':
                            new_chunk = Function(c, c.words, scope)
                        elif scope.name == 'function body':
                            new_chunk = FunctionBody(c, c.words, scope)
                        elif scope.name == 'function params':
                            new_chunk = FunctionParams(c, c.words, scope)
                        else:
                            new_chunk = Chunk(c, c.words, scope)
			
			new_chunk.keep.append(word)

			#print "word"
			#print word
			#print "words"
			#print c.words
			#print "keep"
			#print c.keep
			#print new_chunk.keep

			c.words = process(new_chunk)
										
			c.keep.append(new_chunk)
				
			continue
		
		# end
		for k,b in c.scope.list_key_end: #if term != 0:
			if key == k:
				
				# immediate terminator
				#if term == 1:
				#	ret = c.words
				#	ret.insert(0,word)
				#	c.words = []
				#	return ret
				# return what was not used
				#if word == term:

				# keep or return the end word?
				if b:
					c.keep.append(word)
				else:
					c.words.insert(0,word)
				
				# return all unused words
				ret = c.words
				c.words = []
				
				return ret
		
		# if word is neither a start nor an end, keep it
		c.keep.append(word)
		
	return []


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

def remove_white(words):
    nwords = []
    for w in words:
        #if w in ['','\n']:
        if w in ['']:
            pass
        else:
            nwords.append(w)
    
    return nwords


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


def preprocess(lines):
        lines = fragment(lines, "[\t\ ]+")
	
	lines = fragment(lines, "([\n{}\(\);,])")

        lines = fragment(lines, "(?<!:)(:)(?!:)")

        lines = remove_white(lines)

        return lines















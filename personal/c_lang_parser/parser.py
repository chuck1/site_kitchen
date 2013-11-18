#from termcolor import colored
import curses
import re


stdscr = curses.initscr()




curses.start_color()

curses.init_pair(1,curses.COLOR_BLUE,curses.COLOR_WHITE)
curses.init_pair(2,curses.COLOR_RED,curses.COLOR_WHITE)
curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_WHITE)
curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_WHITE)
curses.init_pair(5,curses.COLOR_YELLOW,curses.COLOR_WHITE)
curses.init_pair(6,curses.COLOR_CYAN,curses.COLOR_WHITE)




if curses.can_change_color() == 1:
	stdscr.addstr( "can change color\n", curses.color_pair(1) )
else:
	stdscr.addstr( "cannot change color\n", curses.color_pair(1) )

#curses.init_color(0,0,0,0)



#stdscr.addstr( "Pretty text", curses.color_pair(1) )



class bclr:
	blue = '\033]95m'
	end = '\033]0m'

def displaysearch(search):
	if search is None:
		return None
	return '<Search: %r, groups=%r>' % (search.group(), search.groups())



class Ref:
	def __init__(self,obj):
		self.obj = obj
	def get(self):
		return self.obj
	def set(self,obj):
		self.obj = obj


gcolor_pair = 0

class Chunk:
	def __init__(self):
		global gcolor_pair
		#self.chunks = []
		#self.text = []
		self.code = 0
		self.words = []
		self.keep = []
		gcolor_pair = gcolor_pair + 1
		if gcolor_pair > 6:
			gcolor_pair = 1
		self.color_pair = gcolor_pair
	def scan(self,term):
		ret = []
		while len(self.words) > 0:
			w = self.words.pop(0)
			# terminator
			if w == term:
				ret.append(w)
				return ret
			# discard
			#if any(w == s for s in discard):
			#	continue
			# neutral
			ret.append(w)
		return ret
	def process(self):
		term = terminator_dict[self.code]
	
		# if chunk has a code, then it was created by another call to process and we should therefore look for an initiator
		if self.code > 0:
			init = initiator_dict[self.code]
			if init != 0:
				self.keep += self.scan(init)
		
		# do until all words are poped
		while len(self.words) > 0:
			# pop words until starter is found
			word = self.words.pop(0)
			#print "%r" % word
			
			s_code = classify_starter(word)
			if s_code > 0:
				
				# create new chunk
				new_chunk = Chunk()
				
				new_chunk.keep.append(word)
				new_chunk.code = s_code
				
				new_chunk.words = self.words
				self.words = new_chunk.process()
				
				
				self.keep.append(new_chunk)
				
				continue	
			if term != 0:
				if term == 1:
					ret = self.words
					ret.insert(0,word)
					self.words = []
					return ret
				# return what was not used
				if word == term:
					self.keep.append(word)
					ret = self.words
					self.words = []
					return ret
			
			# if word is neither a starter nor a terminator, keep it
			self.keep.append(word)
	def cprint(self):
		for k in self.keep:
			if isinstance(k,Chunk):
				k.cprint()
			else:
				stdscr.addstr( k, curses.color_pair(self.color_pair) )
		
	#chunks = []
	#text = []
	code = 0
	words = []
	keep = []
	color_pair = 1
	
#def print_chunk(chunk,pre,a):
#	stdscr.addstr( pre + (">>>%r<<<" % (" ".join(chunk.text)+" "+" ".join(chunk.keep))) + "\n", curses.color_pair(1) )
#	#print pre+"text==>"+" ".join(chunk.text)
#	#print pre+"keep==>"+" ".join(chunk.keep)
#	pre = pre+"\t"
#	for c in chunk.chunks:
#		print_chunk(c,pre,a+1)



def classify_starter(word):
	if len(word) > 0:
		if word[0] == '#':
			return 1
	if word == 'namespace':
		return 2
	if word == 'class':
		return 3
	if re.match("\w+:",word):
		return 4
	return 0



#codes
# 0  unset
# 1  preprocessor
# 2  namespace
# 3  class

terminator_dict = {
	0  : 0,
	1  : "\n",
	2  : '}',
	3  : '}',
	4  : 1,
}

initiator_dict = {
	1  : 0,
	2  : "{",
	3  : "{",
	4  : 0,
}



f = open('test.hpp','r')

pat = re.compile("[^\t ]+")

word_list = []

for line in f:
	words = re.split('([;\s])',line)
	word_list += words



# global chunk
gchunk = Chunk()
gchunk.words = word_list
#process2(gchunk)
gchunk.process()




#print len(gchunk.chunks)
#print len(gchunk.chunks[0].chunks)
#print len(gchunk.chunks[0].chunks[0].chunks)




#print_chunk(gchunk,"",0)
gchunk.cprint()



stdscr.refresh()








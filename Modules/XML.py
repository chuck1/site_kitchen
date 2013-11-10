import re
import sys
import lxml.etree as etree
import logging

def find( element, split, create_missing=False ):
	# element: etree element
	# str: xml abrev string. first entry should match element
	
	logging.debug(split)
	
	#print "last=%r"%last
	
	head = element
	
	if split:
		first = split.pop(0)
		
		if not compare_str( head, first ):
			raise Exception('first not found')
		
		#print "found {0:s}".format(head.tag)
	else:
		raise Exception('only one')

	
	for s in split:
		logging.debug("looking for \"{0:s}\"".format(s))
		
		elements = findall( head, s )
		
		if len(elements) == 0:		
			if create_missing:
				#if an element in the chain doesn't exist, create it
				el_new = construct(s)
				head.append(el_new)
				head = el_new
				
				logging.warning("creating \"{0:s}\" element".format(head.tag))
			else:
				raise Exception('"{0:s}" not found'.format(s))
		elif len(elements) > 1:
			raise Exception('multiple found')
		elif len(elements) == 1:
			#print "found one {0:s}".format(elements[0].tag)
			head = elements[0]
		else:
			raise Exception('wtf')
		
	return head
	
	
def insert( element, split ):
	# element: etree element
	# str: xml abrev string. first entry should match element
	
	logging.debug(split)
	
	last = split.pop()
	
	#print "last=%r"%last

	head = find( element, split, True )	
		
	el = findall( head, last )
	
	if not el:
		el_new = construct( last )
	
		#print "appending {0:s}".format(el_new.tag)
	
		head.append(el_new)
	else:
		logging.warning('exists')
	
	
def compare( element, tag, attr ):
	#print "compare()"
	if element.tag!=tag:
		return 0
	
	for a in attr:
		#print a,attr[a],element.get(a[0])
		if element.get(a) != attr[a]:
			return 0
	
	return 1

def compare_str( element, str ):
	tag,attr,text = parse_element( str )
	
	return compare( element, tag, attr )

def findall( element, str ):
	#print "findall({0:s},{1:s})".format(element,str)
	
	tag,attrs,text = parse_element( str )

	logging.debug("{0} {1}".format(tag,attrs))
	
	#print tag
	
	raw = element.findall(tag)
	
	logging.debug(raw)
	
	el = []

	while raw:
		e = raw.pop(0)
		
		if compare( e, tag, attrs ):
			el.append(e)
	
	return el

def parse_attr( srch_attr ):
	attr={}
	
	list_attr = re.split( ',', srch_attr.group(1) )
	
	for str_attr in list_attr:
		parts = re.split( '=', str_attr )
		
		if len(parts)==2:
			attr[parts[0]] = parts[1]
	
	return attr
	
def parse_element( str ):
	attr = {}
	text = None
	
	srch_attr = re.search( '{(.*)}', str )
	srch_text = re.search('\((.*)\)',str)
	
	if srch_attr:
		tag = re.search( '(.*){', str ).group(1)	
	elif srch_text:
		tag = re.search( '(.*)\(', str ).group(1)
	else:
		tag = str
	
	if srch_attr:
		attr = parse_attr(srch_attr)
	if srch_text:
		text = srch_text.group(1)
	
	return tag,attr,text


def construct( str ):
	tag,attrib,text = parse_element( str )
	
	el = etree.Element( tag, attrib )
	
	if text:
		el.text = text
		
	return el

def test():
	filename = sys.argv[1]
	str = sys.argv[2]

	print "filename=%r" % filename
	print "str=%r" % str

	tree = etree.parse( filename )
	root = tree.getroot()

	insert( root, str )

	tree.write( filename )




#!/usr/bin/env python

import re
import sys
import lxml.etree as etree
import logging

def parse_element(str):
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

def construct(string):
	tag,attrib,text = parse_element(string)
	
	element = etree.Element(tag, attrib)
	
	if text:
		element.text = text
	
	return element

class Element:
	def __init__(self, element):
		self.element = element
	
	
	def find(self, list_string, create_missing=False):
		# element: etree element
		# str: xml abrev string. first entry should match element
		
		logging.debug(list_string)
		
		#print "last=%r"%last
		
		if not list_string:
			return self
		
		first = list_string.pop(0)
		
		child = self.find_child(first, create_missing)
		
		return child.find(list_string, create_missing)
		

	def find_child(self, string, create_missing=False):

		logging.debug("search for \"{0:s}\"".format(str))
		
		elements = self.findall(string)
		
		if len(elements) == 0:		
			if create_missing:
				#if an element in the chain doesn't exist, create it
				new = construct(string)
				self.element.append(new)
				return Element(new)
				
				logging.warning("creating \"{0:s}\" element".format(head.tag))
			else:
				raise Exception('"{0:s}" not found'.format(string))
		elif len(elements) > 1:
			raise Exception('multiple found')
		elif len(elements) == 1:
			#print "found one {0:s}".format(elements[0].tag)
			return Element(elements[0])
		
		
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
	
	def findall(self, string):
		#print "findall({0:s},{1:s})".format(element,str)
		
		tag,attrs,text = parse_element( string )
	
		logging.debug("{0} {1}".format(tag,attrs))
		
		#print tag
		
		raw = self.element.findall(tag)
		
		logging.debug(raw)
		
		el = []
	
		while raw:
			e = raw.pop(0)
			
			if self.compare( e, tag, attrs ):
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
		
	
	
	


if len(sys.argv) < 3:
	print "usage: {0} FILENAME STRING..."
	sys.exit(0)


filename = sys.argv[1]

list_string = []
for i in range(2,len(sys.argv)):
	print "{0:s}".format(sys.argv[0])
	list_string.append(sys.argv[i])



print "filename=%r" % filename
print "list_string={0}".format(list_string)

tree = etree.parse( filename )
root = Element(tree.getroot())

root.find(list_string, True)
tree.write( filename )

	

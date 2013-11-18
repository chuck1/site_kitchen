#!/usr/bin/env pyhton
import os
import lxml.etree as etree

def makeNodes(current, parents, leveldirlist, files):
	new = {}
	for d in leveldirlist:
		child=etree.Element("folder")
		child.set("name",d)
		new[os.path.join(current, d)] = child
		parents[current].append(child)
	for f in files:
		child=etree.Element("page")
		child.set("name",f)
		parents[current].append(child)
	return new

if __name__ == '__main__':
	topdir='html'
	projectxml=etree.Element('folder')
	projectxml.set("name",'html')
	
	root=etree.Element('pages')
	root.append(projectxml)
	
	parents = {topdir: projectxml}
	for current, dirs, files in os.walk(topdir):
		parents.update(makeNodes(current, parents, dirs, files))

	print(etree.tostring(projectxml,pretty_print=True))
	
	tree = etree.ElementTree(root);
	tree.write('test.xml')



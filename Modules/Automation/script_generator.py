import sys
import os
import re
import shutil
import numpy as np
import xml.etree.ElementTree as ET

import Sci.Fluids
import Sci.Data.Flux_Map

# global constants

home_directory = os.environ['HOME']
mohr_directory = "/nfs/mohr/sva/work/rymalc/bin"

scheme_source_directory = home_directory + "/Documents/Programming/Scheme"

var_def = {
		'GEO_SOLAR_WIDTH':'SOLAR_WIDTH',
		'GEO_SOLAR_LENGTH':'SOLAR_LENGTH'
		}


def print_tree(root,tab = 0):
	text = root.text
	if root.text:
		text = re.sub('[\t\n]','',root.text)
	else:
		text = ''
	print "\t" * tab, root.tag, root.attrib, text
	for child in root:
		#print "\t" * tab, child.tag, child.attrib, re.sub('[\t\n]','',child.text)
		print_tree(child, tab + 1)

def text_to_dir(text):
	number = int(text)
	dir = "x{0:04d}".format(number)
	return dir
def strip_white(text):
	#print "before: <<<{0}>>>".format(text)
	text = re.sub('^[\t\n ]*','',text)
	text = re.sub('[\t\n ]*$','',text)
	#print "after:  <<<{0}>>>".format(text)
	return text
def process_array(text):
	lines = re.split('\n',text)
	lines = [strip_white(line) for line in lines]
	lines = [line for line in lines if line]

	test = lines[0]
	test = re.split(',',test)
	
	rows = len(lines)
	cols = len(test)
	
	ret = np.zeros((rows,cols))
	
	for line,i in zip(lines,range(rows)):
		#print line
		for e,j in zip(re.split(',', line), range(cols)):
			ret[i,j] = float(e)
	return ret

class Case:

	var = {}
	
	# functions
	
	def get_var(self, name):
		try:
			return var[name]
		except:
			def_name = var_def[name]
			self.var[name] = self.var[def_name]
			return self.var[name]
	
	
	def load_var(self, child):
		#print child.attrib, child.text
		
		name = child.attrib['name']
		type = child.attrib['type']
		text = child.text

		print "load \"{0}\"".format(name)

		if type == 'string':
			self.var[name] = strip_white(text)
		elif type == 'int':
			self.var[name] = int(strip_white(text))
		elif type == 'float':
			self.var[name] = float(strip_white(text))
		elif type == 'array':
			self.var[name] = process_array(text)
		else:
			raise 0
		
		
	def load_var_from_root(self, root):
		for child in root.findall('var'):
			self.load_var(child)
		for child in root:
			self.load_var_from_root(child)

	def configure(self, lines):
		lines_configured = []
		for line in lines:
			#print line[:-1]
			matches = re.findall("@(\w+)@",line)
			for m in matches:
				if not m in self.var:
					print "no variable \"{0}\" found".format(m)
					print "required in:"
					print line[:-1]
					raise 0
				v = self.var[m]
				line = re.sub("@" + m + "@", "{0}".format(v), line)
			lines_configured.append(line)
			#print line[:-1]
		return lines_configured
	
	
	def get_lines_configured(self, ifilename):
		ifile = open(ifilename,'r')
		lines = ifile.readlines()
		lines = self.configure(lines)
		return lines
	
	def get_root(self, dir):
		filename = dir + '/config.xml'

		print "loading '{0}'".format(filename)

		tree = ET.parse(filename)
		root = tree.getroot()

		self.include_files(root)

		self.load_var_from_root(root)

		self.get_script(dir)

		return root	
	
	
	def get_script(self, dir):
		filename = dir + '/script.py'
		if os.path.isfile(filename):
			variables = {}
			execfile(filename, variables)
			print "executing scricpt \"{0}\"".format(filename)
			variables['func'](self)
	
	def get_xroot(self, root, tag, dir):
		child = root.find(tag)
		if child is None:
			print "'{0}' in '{1}' not found".format(tag,root.tag)
			raise 0
		x = text_to_dir(child.text)
		dir = mohr_directory + '/' + dir + '/' + x
		
		root = self.get_root(dir)
		
		return root
		
	
	def calculate_fluid(self):
		fluid_name = self.var['FLUID']
		self.fluid = Sci.Fluids.Fluid(fluid_name)
	
	def calculate_inlet_rho(self):
		temp = self.var['INLET_TEMPERATURE']
		
		rho = self.fluid.get('density',temp)
		
		self.var['INLET_RHO'] = rho
		
	def calculate_inlet_mass_flow_rate(self):
		f = self.var['SOLAR_FLUX']
		
		t0 = self.var['INLET_TEMPERATURE']
		t1 = self.var['OUTLET_TEMPERATURE']
		
		dh = self.fluid.enthalpy_change(t0,t1)
		
		w = self.get_var('GEO_SOLAR_WIDTH')
		l = self.get_var('GEO_SOLAR_LENGTH') 
		
		m = f * w * l / dh
		
		self.var['INLET_MASS_FLOW_RATE'] = m

	def load_flux_map(self, dir):
		# load flux_map
		#child = case.root.find('flux_map')
		#if not child is None:
		#	print 'found flux map'
			
		#	root_flux_map = self.get_xroot(case.root, 'flux_map', 'Data/Flux_Map')
			
		A,B,x0 = Sci.Data.Flux_Map.process_xy_data(self.var['FLUX_DATA_X'], self.var['FLUX_DATA_Y'])

		#print A,B,x0

		case.var['SOLAR_A'] = A
		case.var['SOLAR_B'] = B

	def include_profile(self, dir):
		shutil.copyfile(dir + '/prof_T.txt', 'build/prof_T.txt')

	def include_files(self, root):
		print "include files for \"{0}\"".format(root.tag)
		for child in root.findall('include'):
			print child.tag, child.attrib
			
			type = child.attrib['type']
			x = text_to_dir(child.text)
			
			dir,fun = include_dict[type]
			
			dir2 = mohr_directory + '/' + dir + '/' + x
			
			root = self.get_root(dir2)
			
			if fun:
				fun(self,dir2)
		


include_dict = {
		'master':['Master',None],
		'design':['Design',None],
		'geometry':['Geometry',None],
		'flux_map':['Data/Flux_Map',Case.load_flux_map],
		'profile':['Data/Profile',Case.include_profile]
		}

#############################################################################

case = Case()

case.var['CWD'] = "hello"

case.root = case.get_root('.')

print_tree(case.root)

#print_tree(root_master)

lines_bc = []

def bc_simple(name):
	lines = case.get_lines_configured(scheme_source_directory + '/Boundary/' + name + '.scm')
	return lines

bc_tags = {
		'inlet_velocity_udf':bc_simple,
		'solar_udf':bc_simple,
		'exterior_temp_profile':bc_simple
		}

case.calculate_fluid()
case.calculate_inlet_rho()
case.calculate_inlet_mass_flow_rate()

# load boundary condition snippets
for child in case.root.find('bc'):
	print child.tag
	func = bc_tags[child.tag]
	lines = func(child.tag)
	lines_bc += lines

lines_generic_fluid = case.get_lines_configured(scheme_source_directory + "/Fluid/" + case.var['FLUID'] + ".scm")

lines = []
lines += case.get_lines_configured(scheme_source_directory + '/generic.scm')
lines += lines_generic_fluid
lines += case.get_lines_configured(scheme_source_directory + '/udf.scm')
lines += lines_bc
lines += case.get_lines_configured(scheme_source_directory + '/generic_solve.scm')


for line in lines:
	#print line[:-1]
	pass

ofilename = 'build/fluent_script.scm'
print "writing output to \"{0}\"".format(ofilename)
with open(ofilename, 'w') as ofile:
	ofile.writelines(lines)

os.system('dos2unix ' + ofilename)



import math
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import itertools

import pygtk

pygtk.require('2.0')
import gtk

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )


class part:
	def __init__(self, name, m):
		self.m = m
		self.name = name
	
class engine:
	def __init__(self, name, m, isp_atm, isp_vac, thrust):
		self.name = name
		self.m = m
		self.isp_atm = isp_atm
		self.isp_vac = isp_vac
		self.thrust = thrust
	def get_isp_vac(self):
		return self.isp_vac
	def get_isp_atm(self):
		return self.isp_atm

	def get_thrust(self):
		return self.thrust
	
class tank:
	def __init__(self, name, m, m_dry):
		self.name = name
		self.m = m
		self.m_dry = m_dry
	def get_m_dry(self):
		return self.m_dry




commandPod         = part("Command Pod", 1.0)
commandPod2        = part("Command Pod Mk2",4.0)

engineLargeSkipper = engine("Skipper", 4.0,  300.0, 350.0, 650.0)
nuclearEngine      = engine("Nuclear", 2.25, 220.0, 800.0,  60.0)

fuelTank1_2        = tank("ft1", 18.0, 2.0)
fuelTank3_2        = tank("ft2", 36.0, 4.0)

parts   = [commandPod, commandPod2]
tanks   = [fuelTank1_2, fuelTank3_2]
engines = [engineLargeSkipper, nuclearEngine]


class Stage:
	def __init__(self):
		self.parts = [0.0]*len(parts)
		self.tanks = [0.0]*len(tanks)
		self.engines = [0.0]*len(engines)

	def get_mass_total(self):
		m = 0.0
		for p,q in itertools.izip(parts,self.parts):
			m += p.m * float(q)
		for p,q in itertools.izip(tanks,self.tanks):
			m += p.m * float(q)
		for p,q in itertools.izip(engines,self.engines):
			m += p.m * float(q)
		return m
	def get_mass_dry(self):
		m = 0.0
		for p,q in itertools.izip(parts,self.parts):
			m += p.m * float(q)
		for p,q in itertools.izip(tanks,self.tanks):
			m += p.m_dry * float(q)
		for p,q in itertools.izip(engines,self.engines):
			m += p.m * float(q)

		return m
	def get_isp_vac(self):
		n = 0.0
		d = 0.0
		for p,q in itertools.izip(engines, self.engines):
			n += p.get_thrust() * q
			d += p.get_thrust() / p.get_isp_vac() * float(q)
		if d > 0:
			return n / d
		else:
			return 0.0
	def get_isp_atm(self):
		n = 0.0
		d = 0.0
		for p,q in itertools.izip(engines, self.engines):
			n += p.get_thrust() * q
			d += p.get_thrust() / p.get_isp_atm() * float(q)
		if d > 0:
			return n / d
		else:
			return 0.0
	def get_thrust(self):
		t = 0.0
		for p,q in itertools.izip(engines, self.engines):
			t += p.get_thrust() * q
		return t

	
class Rocket:
	
	def __init__(self):
		self.stages = []
	
	def add(self, s, q):
		for a in range(q):
			self.stages.append(s)

	def deltav(self):
		dv = []
		m = self.get_m_total_list()
		
		for s in self.stages:
			m.pop(0)
			m_t = sum(m) + s.m_total()
			m_d = sum(m) + s.get_m_dry()
			isp = s.isp() * 9.81
			#print "m_t",m_t
			#print "m_d",m_d
			#print "isp",isp
			
			dv.append( isp * math.log(m_t / m_d) )
		#print dv
		return sum(dv)

	def get_m_total_list(self):
		m = []
		for s in self.stages:
			m.append(s.m_total())
		return m
	def get_m_total(self):
		return sum(self.get_m_total_list())
	def get_m_dry_list(self):
		m = []
		for s in self.stages:
			m.append(s.get_m_dry())
		return m
	def get_m_dry(self):
		return sum(self.get_m_dry_list())
	
	def get_m_ratio(self):
		m_t = self.get_m_total()
		m_d = self.get_m_dry()
		m_f = m_t - m_d
		return m_f / m_t




class stage_gui:

	def update(self, widget, data=None):
		for i in range(len(self.parts)):
			str = self.parts[i].get_text()
			if str:
				self.stage.parts[i] = int(str)

		for i in range(len(self.tanks)):
			str = self.tanks[i].get_text()
			if str:
				self.stage.tanks[i] = int(str)
		
		for i in range(len(self.engines)):
			str = self.engines[i].get_text()
			if str:
				self.stage.engines[i] = int(str)

		
		self.label["mass_total"].set_text("{0}".format(self.stage.get_mass_total()))
		self.label["mass_dry"].set_text("{0}".format(self.stage.get_mass_dry()))
		self.label["isp_vac"].set_text("{0}".format(self.stage.get_isp_vac()))
		self.label["isp_atm"].set_text("{0}".format(self.stage.get_isp_atm()))
		self.label["thrust"].set_text("{0}".format(self.stage.get_thrust()))
		return 0
			
	def delete_event(self, widget, event, data=None):
		# If you return FALSE in the "delete_event" signal handler,
		# GTK will emit the "destroy" signal. Returning TRUE means
		# you don't want the window to be destroyed.
		# This is useful for popping up 'are you sure you want to quit?'
		# type dialogs.
		print "delete event occurred"

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

	def init_buttons(self):
		self.button = [None,None]

		self.button[1] = gtk.Button("Done")
		self.button[1].connect_object("clicked", gtk.Widget.destroy, self.window)
		self.vbox.pack_start(self.button[1], True, True, 0)
		self.button[1].show()

	def init_parts(self):
		self.parts = []
		
		for p in parts:
			
			label_name = gtk.Label(p.name)
			label_mass = gtk.Label(p.m)
			
			self.table.attach(label_name, 0, 1, self.row, self.row+1)
			self.table.attach(label_mass, 1, 2, self.row, self.row+1)
			
			label_name.show()
			label_mass.show()
			
			self.parts.append(gtk.Entry(max=0))
			self.parts[-1].set_text("0")
			self.parts[-1].connect("changed", self.update, None)
			
			self.table.attach(self.parts[-1], 6, 7, self.row, self.row+1)
			
			self.parts[-1].show()
			
			self.row += 1
			

	def init_tanks(self):
		self.tanks = []

		for p in tanks:
			
			label_name = gtk.Label(p.name)
			label_mass = gtk.Label(p.m)
			label_mass_dry = gtk.Label(p.m_dry)

			self.table.attach(label_name,     0, 1, self.row, self.row+1)
			self.table.attach(label_mass,     1, 2, self.row, self.row+1)
			self.table.attach(label_mass_dry, 2, 3, self.row, self.row+1)
			
			label_name.show()
			label_mass.show()
			label_mass_dry.show()
			
			self.tanks.append(gtk.Entry(max=0))
			self.tanks[-1].set_text("0")
			self.tanks[-1].connect("changed", self.update, None)
			
			self.table.attach(self.tanks[-1], 6, 7, self.row, self.row+1)
			
			self.tanks[-1].show()
			
			self.row += 1
			
	def init_engines(self):
		self.engines = []

		for p in engines:
			
			label_name = gtk.Label(p.name)
			label_mass = gtk.Label(p.m)
			label_isp_vac = gtk.Label(p.isp_vac)
			label_isp_atm = gtk.Label(p.isp_atm)
			label_thrust = gtk.Label(p.thrust)
			
			
			self.table.attach(label_name,    0, 1, self.row, self.row+1)
			self.table.attach(label_mass,    1, 2, self.row, self.row+1)
			self.table.attach(label_isp_vac, 3, 4, self.row, self.row+1)
			self.table.attach(label_isp_atm, 4, 5, self.row, self.row+1)
			self.table.attach(label_thrust,  5, 6, self.row, self.row+1)

			label_name.show()
			label_mass.show()
			label_isp_vac.show()
			label_isp_atm.show()
			label_thrust.show()
	

	
			self.engines.append(gtk.Entry(max=0))
			self.engines[-1].set_text("0")
			self.engines[-1].connect("changed", self.update, None)
			
			self.table.attach(self.engines[-1], 6, 7, self.row, self.row+1)
			
			self.engines[-1].show()
			
			self.row += 1
			
		

	def init_label(self):
		
		self.label = {}
		
		headings = ["mass_total","mass_dry","isp_vac","isp_atm","thrust"]
	
		i = 1
		for h in headings:
			self.label[h] = gtk.Label("0")
			self.table.attach(self.label[h], i, i+1, self.row, self.row+1)			
			self.label[h].show()
			i += 1
		
		
	def __init__(self, stage):
		self.stage = stage

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		
		self.vbox = gtk.VBox(False,0)
		self.window.add(self.vbox)
		self.vbox.show()

		self.table = gtk.Table(10,10)
		self.vbox.pack_start(self.table, True, True, 0)
		self.row = 1
		
		
		
		
		
		headings = ["name","mass total","mass dry","isp vac","isp atm","thrust","quantity"]
		
		i = 0
		for h in headings:
			label = gtk.Label(h)
			self.table.attach(label, i, i+1, 0, 1)
			label.show()
			i += 1


		self.init_parts()
		self.init_tanks()
		self.init_engines()
		
		self.table.show()

		self.init_label()

		self.init_buttons()

		self.window.show()
	
	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()


class rocket_gui:
	def delete_event(self, widget, event, data=None):
		# If you return FALSE in the "delete_event" signal handler,
		# GTK will emit the "destroy" signal. Returning TRUE means
		# you don't want the window to be destroyed.
		# This is useful for popping up 'are you sure you want to quit?'
		# type dialogs.
		print "delete event occurred"

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()
	
	def edit_stage(self, widget, stage):
		g = stage_gui(stage)
		g.main()
		
	def new_stage(self, widget):
		s = Stage()
		self.rocket.add(s,1)
		
		
		label_name = gtk.Label("name")
		self.table.attach(label, 0, 1, self.row, self.row+1)
		label.show()
		
		label_deltav = gtk.Label("0.0")
		self.table.attach(label, 1, 2, self.row, self.row+1)
		label.show()
		
		button_edit = gtk.Button("Edit")
		button_edit.connect_object("clicked", self.edit_stage, sef.window, s)
		self.table.attach(button_edit, 2, 3, self.row, self.row+1)
		button_edit.show()
		
		self.row += 1
		
		#button_delete = gtk.Button("Done")
		#button[1].connect_object("clicked", gtk.Widget.destroy, self.window)
		#self.vbox.pack_start(self.button[1], True, True, 0)
		#button[1].show()
		
		self.rows.append((label_name,label_deltav,button_edit))
		
		
	def init_table(self):
		self.table = gtk.Table(10,10)
		self.vbox.pack_start(self.table, True, True, 0)
		self.row = 1
		
		
		headings = ["name","deltav"]
		
		i = 0
		for h in headings:
			label = gtk.Label(h)
			self.table.attach(label, i, i+1, 0, 1)
			label.show()
			i += 1

		self.table.show()
	def __init__(self, rocket):
		self.rocket = rocket
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		
		self.vbox = gtk.VBox(False,0)
		self.window.add(self.vbox)
		self.vbox.show()

		self.init_table()
	
		button = gtk.Button("New")
		button.connect_object("clicked", self.new_stage, self.window)
		self.vbox.pack_start(button, True, True, 0)
		button.show()
		
		self.window.show()
	
	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
	r = Rocket()
	g = rocket_gui(r)
	
	g.main()
	
	







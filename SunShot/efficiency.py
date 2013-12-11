#!/usr/bin/env python
import os
import sys
import numpy as np

import pygtk

pygtk.require('2.0')
import gtk

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

class HelloWorld:

	# This is a callback function. The data arguments are ignored
	# in this example. More on callbacks below.
	def hello(self, widget, data=None):
		n = [0]
		for i in range(1):	
			s = self.entry[i].get_text()
			if s:
				n[i] = float(s)
			else:
				print "empty string"
				return
		
		T = float(self.entry[0].get_text())
		
		T_inf = 298.0
		h_nat = 15.0
		sigma = 5.67 * pow(10,-8)
		emiss = 0.95
		
		q_abs = 1e6
		q_rad = emiss * sigma * (pow(T,4) - pow(T_inf,4))
		q_conv = h_nat * (T - T_inf)
		
		eff = q_abs * emiss / (q_abs + q_rad + q_conv)
		
		self.entry[1].set_text("{0}".format(eff))
		
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

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		
		vbox = gtk.VBox(False,0)
		self.window.add(vbox)
		vbox.show()
		
		self.button = [None,None]

		self.button[0] = gtk.Button("Enter")
		self.button[0].connect("clicked", self.hello, None)
		vbox.pack_start(self.button[0], True, True, 0)
		self.button[0].show()
	
		self.button[1] = gtk.Button("Exit")
		self.button[1].connect_object("clicked", gtk.Widget.destroy, self.window)
		vbox.pack_start(self.button[1], True, True, 0)
		self.button[1].show()

		labels = ["temperature (K)","efficiency"];
		x = [0,0]
		
		self.vbox = []
		self.entry = []
		for i in range(2):
			vb = gtk.VBox(False,0)
			vbox.pack_start(vb, True, True, 0)
			vb.show()
			
			l = gtk.Label(labels[i])
			vb.pack_start(l, True, True, 0)
			l.show()
			
			e = gtk.Entry(max=0)
			e.set_text("{0}".format(x[i]))
			vb.pack_start(e, True, True, 0)
			e.show()
			self.entry.append(e)
			
			self.vbox.append(vb)
		
		
		# and the window
		self.window.show()

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
	hello = HelloWorld()
	
	hello.main()








import sys
import numpy as np
from PyQt4 import QtGui, QtCore
import pylab as pl

import oodb
import unit

class Table(QtGui.QTableWidget):
	def __init__(self, parent):
		super(Table, self).__init__(parent)

		self.itemChanged.connect(self.handleItemChanged)
		self.itemSelectionChanged.connect(self.handleItemSelectionChanged)

		self.windows = []
	
	def event(self, e):
		#print('QtGui.QTableWidget:', e)
		return super(Table, self).event(e)

	def editObject(self):
		print('editObject')
		
		for rng in self.selectedRanges():
			#for c in range(rng.leftColumn(), rng.rightColumn() + 1):
			for r in range(rng.topRow(), rng.bottomRow() + 1):
				print('r',r)
				obj = self.objectAt(r)
				print(obj)
				if obj:
					self.windows.append(oodb.gui.objectedit.Window(obj))
                    

	def refresh(self):

		text1 = self.parent().editext[0].text()
		print('text1',repr(text1))

		text2 = "[" + self.parent().text_fields.toPlainText() + "]"
		print('text1',repr(text2))

		if text1 and text2:
			try:
				res1 = eval(text1)
				res2 = eval(text2)
				#print(res)
			except:
				print(sys.exc_info())
				self.setRowCount(0)
				self.setColumnCount(0)
				return
		else:
			#self.rows = self.db.gen_rows(oodb.class_util.all, ['id', ('type',type), 'desc'])
			#self.rows = self.db.gen_rows(
			#        oodb.class_util.designs,
			#        ['id', ('type',lambda x: str(type(x))), 'Re', 'mdot']
			#        )
			self.rows = []
			self.setRowCount(0)
			self.setColumnCount(0)
			return
        
		view = self.parent().db.gen_rows(res1, res2)
		self.view = view
		
		#print(self.rows)
		
		
		
		#fmt = [Format()]*C
		
		self.setRowCount(view.r)
		self.setColumnCount(view.c)

		# headers
		for c in range(view.c):
			i = oodb.gui.TableWidgetItem(view.headers[c], False)
			self.setItem(0,c,i) 
		
		for r in range(view.r):
			for c in range(view.c):
				v = view.rows[r][c]
				
				print(v,v.get())
				if v.editable:
					print('editable')
					i = oodb.gui.TableWidgetItemRaw(
							view.rows[0][c],
							v.get(),
							v.obj)
				else:
					print('not editable')
					i = oodb.gui.TableWidgetItem(v.get())

				#if isinstance(v, oodb.Value):
				#print('WhatsThis',str(v.obj))

				d = v.get()
				
				i.setToolTip(str(type(d)))
				
				i.setEditable(v.editable)
					
				self.setItem(r+1,c,i)                        

		self.resizeColumnsToContents()
		
		
		
	def contextMenuEvent(self, event):
		self.menu = QtGui.QMenu(self)

		editobjectAction = QtGui.QAction('Edit Object', self)
		editobjectAction.triggered.connect(self.editObject)
		
		self.menu.addAction(editobjectAction)
		# add other required actions
		self.menu.popup(QtGui.QCursor.pos())

	def items(self, rows, col):
		for row in rows:
			yield self.item(row,col)
		
		
	def plot(self):

		ret = self.selectionArray()

		if ret:
			rows = ret[0]
			cols = ret[1]
			arr = ret[2]
			
			print('cols',cols)
			print('arr')
			
			items = list(self.items(rows, cols[0]))
			for i in items:
				print(type(i.value))
			
			for a in arr:
				print(a)
			
			#print(arr[0])
			pl.plot(arr[0], arr[1], 'o')
			
			pl.xlabel(self.item(0, cols[0]).text())
			pl.ylabel(self.item(0, cols[1]).text())
			
			pl.show()

	def selectionArray(self):
			l = self.selectedRanges()
			
			ret = oodb.util.processRange(l)

			if ret:
					rows = ret[0]
					cols = ret[1]

					print('rows cols', rows, cols)
					
					nRows = len(rows)
					nCols = len(cols)

					arr = []
					for c in range(nCols):
							arr.append(np.zeros((nRows)))
					
					for r in range(nRows):
							for c in range(nCols):
									#print('r c', r, c)
									R = rows[r]
									C = cols[c]
									#print('R C', R, C)
									
									i = self.item(R, C)
									#print(i.text())
									
									#arr[c][r] = float(i.text())
									print(type(i.value))
									
									if isinstance(i.value, unit.Value):
										f = float(i.value.v)
									else:
										f = float(i.value)
									
									arr[c][r] = f
			
					return rows, cols, arr
			
			return None
	
	def handleItemSelectionChanged(self):
			print('QtGui.QTableWidget: itemSelectionChanged')

	def objectAt(self, r):
			v = self.rows[r][0]
			if isinstance(v, oodb.Value):
					return v.obj

			return None
			
	def handleItemChanged(self, item):
			if isinstance(item, oodb.gui.TableWidgetItemRaw):
					item.handleChanged()
					return
			
			#print(item, 'changed')
			#print(self.parent())
			
			v = self.view.rows[item.row()-1][item.column()]
			#print(v)
			
			if isinstance(v, oodb.Value) and v.editable:
					#print('edit value')
					setattr(
							v.obj,
							v.name,
							oodb.gui.convert(item.text()))
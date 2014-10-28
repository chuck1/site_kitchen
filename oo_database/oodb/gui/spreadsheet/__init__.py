import sys
import numpy as np
from PyQt4 import QtGui, QtCore
import pylab as pl

import oodb
import oodb.gui.objectedit

from oodb.gui.spreadsheet.Table import Table

class Format:
	def prnt(self, value):
		data = value.get()
		
		if isinstance(data, str):
				return '{}'.format(data)
		elif isinstance(data, int):
				return '{}'.format(data)
		elif isinstance(data, float) or isinstance(data, np.float64):
				return '{:E}'.format(data)
		elif isinstance(data, type):
				return '{}'.format(data)

		return str(data)
		
		print(type(value))
		print(type(data))
		raise Exception('Format.prnt')


        



class TabLayout(QtGui.QVBoxLayout):
        def __init__(self, parent):
                super(TabLayout, self).__init__(parent)


class Tab(QtGui.QWidget):
        def __init__(self, parent, s0, s1):
                super(Tab, self).__init__(parent)

                self.s0 = s0
                self.s1 = s1

                self.w = [[300,100,100],[600],[600]]
                self.h = [60,60,600]

                self.db = oodb.Database()

                #self.widget = QtGui.QWidget(self)

                self.layout = TabLayout(self)

                self.setLayout(self.layout)

                self.createGeneratorTextBox()
                self.createTable()

        def resizeEvent(self, e):
                w = e.size().width()
                h = e.size().height()
                print(self, w, h)

                #self.tb2.resize(w, self.h[1])
                
                #self.tab.resize(w, h - sum(self.h[:2]))
                
        def createGeneratorTextBox(self):

                self.editext = []
                
                # first
                self.editext.append(QtGui.QLineEdit(self.s0, self))

                self.layout.addWidget(self.editext[0])
                
                self.editext[0].resize(self.w[0][0], 60)
                
                self.editext[0].show()

                # second


                
                self.text_fields = QtGui.QTextEdit(self.s1, self)
                
                #self.putInSlot(self.tb2, 0, 1)
                self.layout.addWidget(self.text_fields, 1)
                
                self.text_fields.show()
                
                
                
        def createTable(self):
                
                self.tab = Table(self)

                self.tab.refresh()

                #self.putInSlot(self.tab, 0, 2)
                self.layout.addWidget(self.tab, 5)
                
                self.tab.show()


        def plot(self):
                self.tab.plot()
                
class TabWidget(QtGui.QTabWidget):
    
        def __init__(self, parent, s0, s1):
                super(TabWidget, self).__init__(parent)

                self.s0 = s0
                self.s1 = s1
                
                #self.setStyleSheet('font-size: 11pt; font-family: Courier;')

                self.setTabPosition(QtGui.QTabWidget.South)

                self.initUI()

        def resizeEvent(self, e):
                w = e.size().width()
                h = e.size().height()
                print(self, w, h)

                self.currentWidget().updateGeometry()

                #self.tb2.resize(w, self.h[1])
                
                #self.tab.resize(w, h - sum(self.h[:2]))

        def moveEvent(self, e):
                x = e.pos().x()
                y = e.pos().y()
                #print('move', x, y)
        
        def event(self, e):
                return super(TabWidget, self).event(e)

        def putInSlot(self, o, x, y):
                X = sum(self.w[y][:x])
                Y = sum(self.h[:y])
                w = self.w[y][x]
                h = self.h[y]
                
                o.move(X,Y + 30)
                o.resize(w, h)

                print('x y', x, y)
                print('X Y', X, Y)
                print('w h', w, h)
                print('w h', self.w, self.h)

        def initUI(self):

                self.tabs = []
                self.tabs.append(Tab(self, self.s0, self.s1))
                
                self.addTab(self.tabs[0], "sheet 0")
                
                self.setGeometry(
                        8,
                        31,
                        700,
                        800)

                self.createMenu()
                
                self.setWindowTitle('Quit button')    
                self.show()

        def createMenu(self):
                pass

class Window(oodb.gui.Window):
        def __init__(self, s0, s1):
                super(Window, self).__init__()

                

                self.layout = QtGui.QVBoxLayout()

                self.setLayout(self.layout)

                self.s0 = s0
                self.s1 = s1

                self.createMenuBar()
                self.createTabWidget()
                self.createActions()
                self.show()

        def resizeEvent(self, e):
                w = e.size().width()
                h = e.size().height()
                print(self, w, h)

                #self.tb2.resize(w, self.h[1])
                
                #self.tab.resize(w, h - sum(self.h[:2]))

        def createMenuBar(self):
                self.menubar = QtGui.QMenuBar(self)

                self.layout.addWidget(self.menubar)

        def createActions(self):

                saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Save', self)        
                saveAction.setShortcut('Ctrl+S')
                saveAction.setStatusTip('Save')
                saveAction.triggered.connect(self.tabwidget.currentWidget().db.save)

                exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
                exitAction.setShortcut('Ctrl+Q')
                exitAction.setStatusTip('Exit application')
                exitAction.triggered.connect(QtGui.qApp.quit)

                refreshAction = QtGui.QAction(QtGui.QIcon('refresh.png'), '&Refresh', self)        
                refreshAction.setShortcut('Ctrl+R')
                refreshAction.setStatusTip('Refresh')
                refreshAction.triggered.connect(self.tabwidget.currentWidget().tab.refresh)

                plotAction = QtGui.QAction(QtGui.QIcon('plot.png'), '&Plot', self)        
                plotAction.setShortcut('Ctrl+P')
                plotAction.setStatusTip('Plot')
                plotAction.triggered.connect(self.tabwidget.currentWidget().plot)
                
                #self.statusBar()
                
                fileMenu = self.menubar.addMenu('&File')
                fileMenu.addAction(saveAction)
                fileMenu.addAction(exitAction)
                
                toolsMenu = self.menubar.addMenu('&Tools')
                toolsMenu.addAction(refreshAction)
                toolsMenu.addAction(plotAction)
                
        def createTabWidget(self):

                self.tabwidget = TabWidget(self, self.s0, self.s1)
                
                self.layout.addWidget(self.tabwidget)


class Application(QtGui.QApplication):
        def __init__(self, av):
                super(Application, self).__init__(av)




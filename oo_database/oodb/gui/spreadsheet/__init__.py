import sys
import numpy as np
from PyQt4 import QtGui, QtCore
import pylab as pl

import oodb



class Format:
        def prnt(self, value):
                data = value.prnt()

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
                        res1 = eval(text1)
                        res2 = eval(text2)
                        #print(res)
                        self.rows = self.parent().db.gen_rows(res1, res2)
                else:
                        #self.rows = self.db.gen_rows(oodb.class_util.all, ['id', ('type',type), 'desc'])
                        self.rows = self.db.gen_rows(
                                oodb.class_util.designs,
                                ['id', ('type',lambda x: str(type(x))), 'Re', 'mdot']
                                )

                
                
                #print(self.rows)

                R = len(self.rows)
                C = len(self.rows[0])

                fmt = [Format()]*C
                
                self.setRowCount(R)
                self.setColumnCount(C)

                for r in range(R):
                        for c in range(C):
                                v = self.rows[r][c]
                                i = oodb.gui.TableWidgetItem(
                                        fmt[c].prnt(v)
                                        )

                                #if isinstance(v, oodb.Value):
                                #print('WhatsThis',str(v.obj))

                                d = v.prnt()
                                
                                i.setToolTip(str(type(d)))
                                
                                i.setEditable(v.editable)
                                
                                self.setItem(r,c,i)                        

                self.resizeColumnsToContents()
        
        def contextMenuEvent(self, event):
            self.menu = QtGui.QMenu(self)

            editobjectAction = QtGui.QAction('Edit Object', self)
            editobjectAction.triggered.connect(self.editObject)
            
            self.menu.addAction(editobjectAction)
            # add other required actions
            self.menu.popup(QtGui.QCursor.pos())

        def plot(self):

                ret = self.selectionArray()

                if ret:
                        rows = ret[0]
                        cols = ret[1]
                        arr = ret[2]
                        
                        print('cols',cols)
                        print('arr')
                        
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
                                        arr[c][r] = float(i.text())
                
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
                #print(item, 'changed')
                #print(self.parent())
                
                v = self.rows[item.row()][item.column()]
                #print(v)
                
                if isinstance(v, oodb.Value) and v.editable:
                        #print('edit value')
                        setattr(
                                v.obj,
                                v.name,
                                oodb.gui.convert(item.text()))


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
                
                self.setStyleSheet('font-size: 11pt; font-family: Courier;')

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

class Window(QtGui.QWidget):
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




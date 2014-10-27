from PyQt4 import Qt, QtGui, QtCore

import oodb.gui.spreadsheet
import oodb.gui.objectedit

def convert(s):
        try:
                return int(s)
        except:
                pass

        try:
                return float(s)
        except:
                pass

        return s

class TableWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, string):
        super(TableWidgetItem, self).__init__(string)

    def setEditable(self, x):
        if x:
            f = self.flags()
            f |= 2
            self.setFlags(f)
        else:
            f = self.flags()
            f ^= 2
            self.setFlags(f)

    def handleChanged(self):
        pass

class TableWidgetItemRaw(TableWidgetItem):
    def __init__(self, field_name, value, obj):
        super(TableWidgetItemRaw, self).__init__(str(value))

        self.field_name = field_name
        self.value      = value
        self.obj        = obj

    def handleChanged(self):
        print(self,'handleItemChanged')
        setattr(
            self.obj,
            self.field_name,
            convert(self.text()))

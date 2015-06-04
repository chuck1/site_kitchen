import os
import array
import xml.etree.ElementTree as et
import pickle
import re

def match_int(s):
    return re.match('^\d+$', s)

def match_float(s):
    m1 = re.match('^\d+\.\d*$', s)
    m2 = re.match('^\d*\.\d+$', s)

    if m1:
        return m1
    elif m2:
        return m2
    else:
        return None

class Cell(object):
    def __init__(self, s=None):
        self.set_value(s)

    def set_value(self, s):
        if not s:
            self.dtype = 'none'
            self.v = None
        else:
            if s[0] == '=':
                self.dtype = 'formula'
                self.v = s
            else:
                m = match_int(s)
                if m:
                    self.dtype = 'int'
                    self.v = int(s)
                else:
                    m = match_float(s)
                    if m:
                        self.dtype = 'float'
                        self.v = float(s)
                    else:
                        self.dtype = 'str'
                        self.v = s

    def get_value(self, sheet):
        if self.dtype == 'formula':
            func_cell = lambda r,c: sheet.get_cell(r,c).get_value(sheet)
            _globals = {'cell':func_cell}
            return eval(self.v[1:], _globals)
        else:
            return self.v
    
    def str_type(self):
        return str(self.dtype)

    def str_value(self, sheet):
        return str(self.get_value(sheet))

class Sheet(object):
    def __init__(self):
        self.table = [[Cell()]]

    def num_col(self):
        a = 0
        for row in self.table:
            a = max(a,len(row))
        return a

    def add_row(self):
        row = [Cell()]*self.num_col()
        self.table.append(row)

    def add_col(self):
        for row in self.table:
            c = Cell()
            c.set_value(None)
            row.append(c)

    def set_cell(self, r, c, v):
        while len(self.table) <= r:
            self.add_row()
        
        while self.num_col() <= c:
            self.add_col()

        self.table[r][c].set_value(v)
        
    def get_cell(self, r, c):
        try:
            row = self.table[r]
        except IndexError as e:
            return "row index error"
        
        try:
            col = row[c]
        except IndexError as e:
            return "col index error"
        
        return col
    
    def html_col(self, row, r, c, func):

        td = 0
        td = et.Element('td')
        
        form = et.SubElement(td, 'form', attrib={'id':"form{}_{}".format(r,c)})
        
        t = et.SubElement(form, 'input', attrib={
            'id'  :"{}_{}".format(r,c),
            'type':"text",
            'name':"text"
            })
        
        h = et.SubElement(form, 'input', attrib={
            'type':'hidden',
            'name':'cell',
            'value':"{}_{}".format(r,c),
            })
        
        if c < len(row):
            if row[c]:
                #t.attrib["value"] = row[c].__unicode__()
                t.attrib["value"] = func(row[c], self)
            else:
                t.attrib["value"] = ""
        else:
            t.attrib["value"] = ""

        return td

    def html(self, func):

        table = et.Element('table')

        for row,r in zip(self.table, range(len(self.table))):
            
            tr = et.Element('tr')

            for c in range(self.num_col()):
                tr.append(self.html_col(row, r, c, func))
            
            table.append(tr)

        return et.tostring(table)


class Service(object):
    def __init__(self):
        self.sheet = Sheet()

        self.fifo_name_srv_w = "/tmp/python_spreadsheet_srv_w"
        self.fifo_name_cli_w = "/tmp/python_spreadsheet_cli_w"

        try:
            os.mkfifo(self.fifo_name_srv_w)
            os.mkfifo(self.fifo_name_cli_w)
        except OSError:
            pass

    def write(self, s):
        with open(self.fifo_name_srv_w, 'wb') as f:
            f.write(s)
    
    def read(self):
        with open(self.fifo_name_cli_w, 'rb') as f:
            return f.read()

    def parse_cell(self, s):
        m = re.match('^(\d+)_(\d+)$', s)
        r = int(m.group(1))
        c = int(m.group(2))
        return r,c

    def run(self):
        
        while True:

            #a = array.array('i')

            s = self.read()
            #a.fromstring(s)

            print 's =',s

            if s == 'get sheet':
                s_out = pickle.dumps(self.sheet)
                self.write(s_out)
            elif s == 'add row':
                self.sheet.add_row()
                self.write('0')
            elif s == 'add col':
                self.sheet.add_col()
                self.write('0')
            elif s == 'set cell':
                #cell = self.read()
                #text = self.read()
                #print 'cell =',cell,'text =',text
                self.write('0')
                
                cell = self.read()
                self.write('0')
                
                text = self.read()
                self.write('0')
               
                print 'cell =',cell
                print 'text =',text

                r,c = self.parse_cell(cell)

                print 'r,c = ',r,c
          
                self.sheet.set_cell(r, c, text)

            #print a

        










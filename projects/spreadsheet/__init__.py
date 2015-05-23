
class Element(object):
    def __init__(self, name, attr={}):
        self.name = name
        self.attr = attr
        self.text = list()

        print "__init__", self, self.name, self.text

    def add_child(self, c):
        if self == c:
            raise ValueError

        self.text.append(c)

    def html(self, prefix):

        print "__str__", self.name, repr(prefix), len(self.text)

        ret = ""

        attr_text = " ".join("{}=\"{}\"".format(k,v) for k,v in self.attr.iteritems())

        ret += prefix + "<{} {}>".format(self.name, attr_text)
        
        if self.text:
            ret += "\n"
            if isinstance(self.text, list):

                #print self.text

                for t in self.text:
                    if isinstance(t, Element):

                        if self == t:
                            raise ValueError

                        ret += t.html(prefix + "    ")
                        
                    else:
                        ret += prefix + "    {}\n".format(t)
            else:
                raise ValueError

            ret += prefix
        
        ret += "</{}>\n".format(self.name)

        return ret

    def debug(self):
        print "debug", self, self.name, self.text

        for t in self.text:
            if isinstance(t, Element):
                if self == t:
                    raise ValueError
                else:
                    t.debug()

class Sheet(object):
    def __init__(self):
        self.table = []
        self.num_col = 0

    def set(self, r, c, v):
        while len(self.table) <= r:
            self.table.append([])

        row = self.table[r]

        while len(row) <= c:
            row.append([])
       
        self.num_col = max(self.num_col, c+1)

        row[c] = v
        
    def cell(self, r, c):
        try:
            row = self.table[r]
        except IndexError as e:
            return "row index error"
        
        try:
            col = row[c]
        except IndexError as e:
            return "col index error"

        return col
    
    def html_col(self, row, c):
        print c

        td = 0
        td = Element("td")
                
        e = Element("input", {"type":"text", "name":"cell"})

        if c < len(row):
            if row[c]:
                e.attr["value"] = row[c]
            else:
                e.attr["value"] = ""
        else:
            e.attr["value"] = ""

        td.text.append(e)
           
        return td

    def html(self, prefix):

        ret = ""

        for row in self.table:
            
            tr = Element("tr")

            print "num_col", self.num_col

            for c in range(self.num_col):
                tr.add_child(self.html_col(row, c))

            tr.debug()

            ret += tr.html(prefix)

        return ret









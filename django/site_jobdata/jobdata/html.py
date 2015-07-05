
import xml.etree.ElementTree as et

def has_field(j, f):
    if isinstance(j, dict):
        if j.has_key(f):
            return True
        #else:
        #    print 'object',
        #    print "\n".join(list("  {}:{}".format(k,str(v)) for k,v in j.items()))

    return False

def json_to_element_list(j,path):
    t = et.Element('table')
  
    cnt = 0
    for v in j:
        p = path + [cnt]

        r = et.SubElement(t, 'tr')
       
        #if isinstance(v, dict):
        if has_field(v, 'version'):
            attrib = {
                    'type':'checkbox',
                    'name':",".join(list(str(x) for x in p)),
                    'checked':'',
                    }

            # checkbox
            d = et.SubElement(r, 'td')
            i = et.SubElement(r, 'input', attrib=attrib)
        # data
        d = et.SubElement(r, 'td')

        if isinstance(v, dict):
            d.append(json_to_element(v, p))

        elif isinstance(v, list):
            if v:
                d.append(json_to_element_list(v, p))

        else:
            d.text = str(v)

        cnt += 1

    return t

def json_to_element(j,path):
    t = et.Element('table', attrib={'class':'json'})
    
    for k,v in j.items():
        r = et.SubElement(t, 'tr')
        
        d = et.SubElement(r, 'th')
        d.text = k+':'
       
        d = et.SubElement(r, 'td')

        if isinstance(v, dict):
            d.append(json_to_element(
                v,
                path + [k]))
        elif isinstance(v, list):
            if v:
                d.append(json_to_element_list(
                    v,
                    path + [k]))
        else:
            d.text = str(v)
        
    return t

def json_to_html(j):
    t = json_to_element(j,[])
    return et.tostring(t)

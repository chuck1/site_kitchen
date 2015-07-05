
import xml.etree.ElementTree as et

def has_field(j, f):
    """
    first check if j is dict, then check for key
    """
    if isinstance(j, dict):
        if j.has_key(f):
            return True
        #else:
        #    print 'object',
        #    print "\n".join(list("  {}:{}".format(k,str(v)) for k,v in j.items()))

    return False

def json_to_element_list(j,sel_id,path,paths):
    t = et.Element('table')
  
    cnt = 0
    for v in j:
        p = path + [cnt]

        r = et.SubElement(t, 'tr')
       
        #if isinstance(v, dict):
        if has_field(v, 'version'):
            attrib = {
                    'type':'checkbox',
                    'name':"selector_" + ",".join(list(str(x) for x in p)),
                    }
            
            # if json has _selector entry, use that value, else use default of True
            try:
                o = v['_selector'][str(sel_id)]
            except:
                attrib['checked'] = ''
            else:
                if o:
                    attrib['checked'] = ''

            # add path to paths output
            paths.append(p)

            # checkbox
            d = et.SubElement(r, 'td')
            i = et.SubElement(r, 'input', attrib=attrib)
        # data
        d = et.SubElement(r, 'td')

        if isinstance(v, dict):
            if v:
                e,paths = json_to_element(v,sel_id, p, paths)
                d.append(e)

        elif isinstance(v, list):
            if v:
                e,paths = json_to_element_list(v,sel_id, p, paths)
                d.append(e)

        else:
            d.text = str(v)

        cnt += 1

    return t,paths

def json_to_element(j,sel_id,path,paths):
    """
    create an html table displaying the contents of a json dict object
    """
    t = et.Element('table', attrib={'class':'json'})
    
    for k,v in j.items():
        # do not display the _selector field
        if k == '_selector':
            continue

        r = et.SubElement(t, 'tr')
        
        d = et.SubElement(r, 'th')
        d.text = k+':'
       
        d = et.SubElement(r, 'td')

        if isinstance(v, dict):
            if v:
                e,paths = json_to_element(
                    v,
                    sel_id,
                    path + [k],
                    paths)
                d.append(e)
        elif isinstance(v, list):
            if v:
                e,paths = json_to_element_list(
                    v,
                    sel_id,
                    path + [k],
                    paths)
                d.append(e)
        else:
            d.text = str(v)
        
    return t,paths

def json_to_html(j,sel_id):
    t,paths = json_to_element(j,sel_id,[],[])
    return et.tostring(t),paths


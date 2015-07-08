
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


def json_to_element_list(j, sel_id, path, paths, filter_function):
    """
    warning j must be unfiltered or else list indices could be wrong
    """
    t = et.Element('table')
  
    paths_temp = []
    
    return_none = True
    
    cnt = 0
    for v in j:
        p = path + [cnt]
        cnt += 1

        #print p

        # perform auxilary filter here
        # if element is filtered out, it will not
        # appear in the paths list and it will not
        # be displayed in html
        if not filter_function(v):
            continue
            pass

        return_none = False

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
            paths_temp.append(p)

            # checkbox
            d = et.SubElement(r, 'td')
            i = et.SubElement(r, 'input', attrib=attrib)
        # data
        d = et.SubElement(r, 'td')

        if isinstance(v, dict):
            if v:
                e,paths = json_to_element(v,sel_id, p, paths, filter_function)
                d.append(e)

        elif isinstance(v, list):
            if v:
                e,paths = json_to_element_list(v,sel_id, p, paths, filter_function)
                d.append(e)

        else:
            d.text = str(v)

    paths += paths_temp
    
    if return_none:
        return None,paths
    else:
        return t,paths

def json_to_element(j,sel_id,path,paths, filter_function):
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
                    paths, filter_function)
                if e is not None:
                    d.append(e)
        elif isinstance(v, list):
            if v:
                e,paths = json_to_element_list(
                    v,
                    sel_id,
                    path + [k],
                    paths, filter_function)
                if e is not None:
                    d.append(e)
        else:
            d.text = str(v)
        
    return t,paths

def json_to_html(j,sel_id, filter_function):
    t,paths = json_to_element(j,sel_id,[],[], filter_function)
    return et.tostring(t),paths


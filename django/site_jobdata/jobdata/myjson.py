import json

def json_is_list_of_dict(j):
    if not isinstance(j, list):
        return False

    if not j:
        return True

    for v in j:
        if not isinstance(v, dict):
            return False
    
    return True

def json_list_of_dict_field_any(j, field):
    if not json_is_list_of_dict(j):
        return ValueError("not list_of_dict")
    
    return any(v.has_key(field) for v in j)

def json_list_of_dict_field_all(j, field):
    if not json_is_list_of_dict(j):
        return ValueError("not list_of_dict")
    
    return all(v.has_key(field) for v in j)

def json_is_dict_list_with_field(j, field):
    if not isinstance(j, list):
        raise ValueError("not a list")

    if not j:
        return False

    cnt = 0

    for v in j:
        if not isinstance(v, dict):
            return False

        # v is a dict
        if v.has_key(field):
            cnt += 1

    if cnt > 0:
        return True
    
    return False

def json_dict_list_add_field_if_not_exists(j, field, val):
    if not json_is_list_of_dict(j):
        raise ValueError("not a list_of_dict")

    for v in j:
        if not v.has_key(field):
            v[field] = val

def json_dict_list_add_field_if_not_exists_rec(j, field, val):
    #print "json_dict_list_add_field_if_not_exists_rec"

    if isinstance(j, dict):
        #print "dict"
        for k,v in j.items():
            #print "  "+k
            json_empty_version_rec(v)
    elif isinstance(j, list):
        if json_is_dict_list_with_field(j, field):
            #print "    is_dict_list_with_field"
            json_dict_list_add_field_if_not_exists(j, field, val)
        else:
            for v in j:
                json_empty_version_rec(v)

def json_iter_test(j, test):
    #print "json_iter_test"
    if test(j):
        #print "yield",j
        yield j
    
    if isinstance(j, dict):
        for k,v in j.items():
            for x in json_iter_test(v, test):
                yield x
    elif isinstance(j, list):
        for v in j:
            for x in json_iter_test(v, test):
                yield x

def json_iter_list_of_dict(j):
    #print "json_iter_list_of_dict"
    return json_iter_test(j, json_is_list_of_dict)

def json_path(j, path):
    for p in path:
        try:
            j = j[int(p)]
        except:
            j = j[p]
    return j





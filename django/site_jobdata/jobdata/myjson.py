import json

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
    if not isinstance(j, list):
        raise ValueError("not a list")

    for v in j:
        if not isinstance(v, dict):
            raise ValueError("not a dict")
        
        if not v.has_key(field):
            v[field] = val

def json_empty_version_rec(j):
    
    if isinstance(j, dict):
        for k,v in j.items():
            json_empty_version_rec(v)
    elif isinstance(j, list):
        if json_is_dict_list_with_field(j, 'version'):
            json_dict_list_add_field_if_not_exists(j, 'version', [])

def json_empty_version(person):
    j = person.file_read_json()
    
    json_empty_version_rec(j)

    person.file_save_json(j)
    

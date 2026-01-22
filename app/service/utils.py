def str_to_json(string: str):
    if ':' not in string:
        raise
    if "'"  in string or "\"" in string:
        string = string.replace("'", '').replace("\"", '')
    if ', 'in string:
        string = string.replace(", ", ',')
    print(string)
    if ',' in string:
        objs = string.split(',')
    else:
        objs = [string]
    
    json = {}
    for obj in objs:
        if ':' in obj:
            if obj.index(':') != 0:
                tpl = obj.split(':')
                print(tpl)
                json |= {tpl[0]: tpl[1]}

    return json



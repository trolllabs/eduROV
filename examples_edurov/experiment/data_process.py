def response_parser(not_used, path):
    if isinstance(not_used,str):
        print('wow')
    if isinstance(path, str):
        print('path ' + path)
        if path.startswith('new_participant'):
            print('yep')
        return None
    else:
        print('nope')
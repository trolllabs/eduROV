def response_parser(not_used, path):
    print('not ' + not_used)
    print('path ' + path)
    if path.startswith('new_participant'):
        print('yep')
    return None
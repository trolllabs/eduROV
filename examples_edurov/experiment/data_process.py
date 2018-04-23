def response_parser(not_used, path):
    if path.startswith('/new_participant'):
        form_raw = path[path.find('?') + 1:].split('&')
        form_data = {}
        for field in form_raw:
            pair = field.split('=')
            form_data.update({pair[0]:pair[1]})
        print(form_data)
    return 'redirect=/'
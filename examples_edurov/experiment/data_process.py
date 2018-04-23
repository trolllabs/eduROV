def response_parser(not_used, path):
    if path.startswith('/new_participant'):
        form_data = path[path.find('?') + 1:]
        print(form_data.split('&'))
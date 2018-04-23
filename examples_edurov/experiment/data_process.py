from db import DB


def response_parser(not_used, path):
    db = DB()
    if path.startswith('/new_participant'):
        form_raw = path[path.find('?') + 1:].split('&')
        form_data = {}
        for field in form_raw:
            pair = field.split('=')
            form_data.update({pair[0]:int(pair[1])})
        db.new_actor(age=form_data['age'],
                     gender=form_data['gender'],
                     game_consumption=form_data['game'])
        return 'redirect=/index.html'
    else:
        return None

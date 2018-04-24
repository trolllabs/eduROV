from db import DB


def form_to_dict(path):
    form_raw = path[path.find('?') + 1:].split('&')
    form_data = {}
    for field in form_raw:
        pair = field.split('=')
        form_data.update({pair[0]: pair[1]})
    return form_data


def response_parser(not_used, path):
    db = DB()
    if path.startswith('/new_participant'):
        form_data = form_to_dict(path)
        db.new_actor(
            nickname=form_data['nickname'],
            age=form_data['age'],
            gender=form_data['gender'],
            game_consumption=form_data['game']
        )
        return 'redirect=/index.html'
    elif path.startswith('/actors'):
        return db.all_actors_html()
    elif path.startswith('/highscore'):
        return db.highscore_html()
    elif path.startswith('/new_hit'):
        form_data = form_to_dict(path)
        actor_id = db.last_id()
        db.new_hit(actor_id=actor_id,
                   button=form_data['button'])
        return 'Hit registered'
    else:
        return None

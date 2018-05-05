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
        return db.next_page()
    elif path.startswith('/actors'):
        return db.all_actors_html()
    elif path.startswith('/highscore'):
        return db.highscore_html()
    elif path.startswith('/new_hit'):
        # /new_hit?button=2
        form_data = form_to_dict(path)
        exp = db.current_experiment()
        if exp:
            db.new_hit(
                actor_id=db.last_id(),
                experiment=exp,
                button=form_data['button'])
            return 'Hit registered for experiment {}'.format(exp)
        else:
            msg ='No active experiment'
            print(msg)
            return msg
    elif path.startswith('/participant_finished'):
        db.actor_finished(actor_id=db.last_id())
        return 'Finished participant registered'
    elif path.startswith('/experiment_change'):
        # /experiment_change?change=start
        form_data = form_to_dict(path)
        exp = db.relevant_experiment()
        db.experiment_change(
            actor_id=db.last_id(),
            experiment=exp,
            change=form_data['change'])
        return 'Experiment change registered'


    elif path.startswith('/survey_post'):
        print('/survey_post')
        form_data = form_to_dict(path)
        # process survey data
        return db.next_page()
    elif path.startswith('/next'):
        print('/next')
        return db.next_page()
    else:
        return None

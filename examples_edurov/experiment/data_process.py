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

    elif path.startswith('/new_keydown'):
        exp = db.current_experiment()
        if exp is not None:
            db.new_keydown(actor_id=db.last_id,
                           exp=exp)

    elif path.startswith('/new_hit'):
        # /new_hit?button=2
        form_data = form_to_dict(path)
        exp = db.current_experiment()
        if exp is not None:
            db.new_hit(
                actor_id=db.last_id(),
                experiment=exp,
                button=form_data['button'])
            return 'Hit registered for experiment {}'.format(exp)
        else:
            print('No active experiment')
            return 'No active experiment'

    elif path.startswith('/participant_finished'):
        db.actor_finished(actor_id=db.last_id())
        return 'Finished participant registered'

    elif path.startswith('/experiment_change'):
        # /experiment_change?change=start
        form_data = form_to_dict(path)
        db.experiment_change(
            actor_id=db.last_id(),
            experiment=form_data['exp'],
            change=form_data['change'])
        return 'Experiment change registered'

    elif path.startswith('/survey_post'):
        # /survey_post.php?mental=10&physical=10&temporal=10&effort=10
        # &performance=10&frustration=10&delay=500
        form_data = form_to_dict(path)
        exp = db.last_experiment()
        db.add_survey(actor_id=db.last_id(),
                      experiment=exp,
                      difficulty=form_data['difficulty'])
        return db.next_page()

    elif path.startswith('/next'):
        return db.next_page()

    else:
        return None

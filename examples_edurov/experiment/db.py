# -*- coding: utf-8 -*-
import argparse
import datetime as dt
import sqlite3
import time
from os import path


class DB:
    db_name = 'data.db'
    db_path = path.join(path.dirname(__file__), db_name)
    table_style = '''
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 5px;
            text-align: left;    
        }'''

    inf = '/displays/info.html'
    exp0 = '/displays/experiment0.html'
    exp1 = '/displays/experiment1.html'
    exp2 = '/displays/experiment2.html'
    sur = '/forms/survey.html'
    fin = '/displays/finish.html'

    crowd0_exp = [None, 0, None, 1, None, 2, None, None]
    crowd1_exp = [None, 0, None, 2, None, 1, None, None]
    crowd2_exp = [None, 1, None, 0, None, 2, None, None]
    crowd3_exp = [None, 1, None, 2, None, 0, None, None]
    crowd4_exp = [None, 2, None, 0, None, 1, None, None]
    crowd5_exp = [None, 2, None, 1, None, 0, None, None]
    crowds_exp = {0: crowd0_exp,
                  1: crowd1_exp,
                  2: crowd2_exp,
                  3: crowd3_exp,
                  4: crowd4_exp,
                  5: crowd5_exp}

    crowd0_order = [inf, exp0, sur, exp1, sur, exp2, sur, fin]
    crowd1_order = [inf, exp0, sur, exp2, sur, exp1, sur, fin]
    crowd2_order = [inf, exp1, sur, exp0, sur, exp2, sur, fin]
    crowd3_order = [inf, exp1, sur, exp2, sur, exp0, sur, fin]
    crowd4_order = [inf, exp2, sur, exp0, sur, exp1, sur, fin]
    crowd5_order = [inf, exp2, sur, exp1, sur, exp0, sur, fin]
    crowds_order = {0: crowd0_order,
                    1: crowd1_order,
                    2: crowd2_order,
                    3: crowd3_order,
                    4: crowd4_order,
                    5: crowd5_order}

    def __init__(self):
        if not path.isfile(self.db_path):
            self.createdb()

        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        with open(path.join(path.dirname(__file__), 'table.html'), 'r') as f:
            self.table_base = f.read()

    @classmethod
    def createdb(cls):
        if not path.isfile(cls.db_path):
            conn = sqlite3.connect(cls.db_path)
            c = conn.cursor()
            c.execute("""CREATE TABLE actors (
                age integer,
                gender integer,
                education integer,
                game integer,
                computer integer,
                eye integer,
                nickname text, 
                position integer,
                start real,
                starttxt text,
                end real,
                endtxt text,
                crowd integer,
                startexp0 real,
                startexp1 real,
                startexp2 real,
                endexp0 real,
                endexp1 real,
                endexp2 real,
                tothitsexp0 integer,
                tothitsexp1 integer,
                tothitsexp2 integer,
                keydowns0 integer,
                keydowns1 integer,
                keydowns2 integer,
                tothits integer,
                valid integer
                )""")
            c.execute("""CREATE TABLE hits (
                actor integer,
                experiment integer,
                button integer,
                time integer
                )""")
            c.execute("""CREATE TABLE survey (
                actor integer,
                experiment integer,
                mental integer,
                physical integer,
                temporal integer,
                effort integer,
                performance integer,
                frustration integer,
                delay integer,
                time integer
                )""")
            conn.commit()
            conn.close()
            print('db: created DB at {}'.format(cls.db_path))
        else:
            raise FileExistsError('{} already exist'.format(cls.db_path))

    @classmethod
    def check(cls):
        if path.isfile(cls.db_path):
            print('found file')
        else:
            print('did not find file')

    def actor_dict(self, actor_id):
        self.c.execute(
            """SELECT position, crowd FROM actors WHERE rowid='{}'"""
                .format(actor_id))
        position, crowd = self.c.fetchone()
        return {'position': position,
                'crowd': crowd}

    def next_page(self):
        actor_id = self.last_id()
        dic = self.actor_dict(actor_id)
        next = dic['position'] + 1
        crowd = dic['crowd']
        newpage = self.crowds_order[crowd][next]

        with self.conn:
            self.c.execute(
                """UPDATE actors SET position={} 
                WHERE rowid={} LIMIT 1""".format(next, actor_id))

        if newpage == '/displays/finish.html':
            self.actor_finished(actor_id=self.last_id())

        return 'redirect={}'.format(newpage)

    def last_id(self):
        self.c.execute("""SELECT rowid FROM actors ORDER BY rowid DESC""")
        return self.c.fetchone()[0]

    def set_keydowns(self, actor_id, exp, amount):
        data = {
            'exp': exp,
            'actor_id': actor_id,
            'amount': amount
        }
        with self.conn:
            self.c.execute(
                """UPDATE actors SET keydowns{exp}={amount} 
                WHERE rowid={actor_id} LIMIT 1""".format(**data),
            )
        print('db: keydowns added')

    def current_experiment(self):
        self.c.execute("""SELECT position, crowd, startexp0, startexp1, 
        startexp2 FROM actors ORDER BY rowid DESC LIMIT 1""")
        position, crowd, st0, st1, st2 = self.c.fetchone()
        exp = self.crowds_exp[crowd][position]
        if exp == 0 and st0:
            return 0
        elif exp == 1 and st1:
            return 1
        elif exp == 2 and st2:
            return 2
        else:
            return None

    def last_experiment(self):
        self.c.execute("""SELECT position, crowd FROM actors ORDER BY rowid 
        DESC LIMIT 1""")
        position, crowd = self.c.fetchone()
        return self.crowds_exp[crowd][position - 1]

    def add_survey(self, actor_id, experiment, form):
        data = {'actor': actor_id,
                'experiment': experiment,
                'mental': form['mental'],
                'physical': form['physical'],
                'temporal': form['temporal'],
                'effort': form['effort'],
                'performance': form['performance'],
                'frustration': form['frustration'],
                'delay': form['delay'],
                'time': time.time()
                }
        query = """INSERT INTO survey (actor, experiment, mental, 
        physical, temporal, effort, performance, frustration, delay, time) 
        VALUES (:actor, :experiment, :mental, :physical, :temporal, 
        :effort, :performance, :frustration, :delay, :time)"""
        with self.conn:
            self.c.execute(query, data)
        print('db: survey added')

    def next_crowd(self):
        self.c.execute("""SELECT * FROM actors WHERE crowd='0'""")
        crowd_0 = len(self.c.fetchall())
        self.c.execute("""SELECT * FROM actors WHERE crowd='1'""")
        crowd_1 = len(self.c.fetchall())
        self.c.execute("""SELECT * FROM actors WHERE crowd='2'""")
        crowd_2 = len(self.c.fetchall())
        self.c.execute("""SELECT * FROM actors WHERE crowd='3'""")
        crowd_3 = len(self.c.fetchall())
        self.c.execute("""SELECT * FROM actors WHERE crowd='4'""")
        crowd_4 = len(self.c.fetchall())
        self.c.execute("""SELECT * FROM actors WHERE crowd='5'""")
        crowd_5 = len(self.c.fetchall())
        totals = {0: crowd_0,
                  1: crowd_1,
                  2: crowd_2,
                  3: crowd_3,
                  4: crowd_4,
                  5: crowd_5}
        smallest = 999
        smallest_crowd = 0
        for crowd in totals:
            if totals[crowd] < smallest:
                smallest_crowd = crowd
                smallest = totals[crowd]
        return smallest_crowd

    def new_actor(self, form):
        timestamp = time.time()
        data = {
            'age': form['age'],
            'gender': form['gender'],
            'education': form['education'],
            'game': form['game'],
            'computer': form['computer'],
            'eye': form['eye'],
            'nickname': form['nickname'],
            'start': timestamp,
            'starttxt': dt.datetime.fromtimestamp(timestamp).strftime(
                '%Y-%m-%d %H:%M'),
            'crowd': self.next_crowd(),
            'position': -1
        }
        query = """INSERT INTO actors (age, gender, education, 
        game, computer, eye, nickname, start, starttxt, crowd, position) 
        VALUES (:age, :gender, :education, :game, :computer, 
        :eye, :nickname, :start, :starttxt, :crowd, :position)"""

        with self.conn:
            self.c.execute(query, data)
        print('db: new actor created')

    def update_total_hits(self, actor_id):
        self.c.execute(
            """SELECT * FROM hits WHERE actor='{}' AND experiment='0'"""
                .format(actor_id))
        hits_exp_0 = len(self.c.fetchall())
        self.c.execute(
            """SELECT * FROM hits WHERE actor='{}' AND experiment='1'"""
                .format(actor_id))
        hits_exp_1 = len(self.c.fetchall())
        self.c.execute(
            """SELECT * FROM hits WHERE actor='{}' AND experiment='2'"""
                .format(actor_id))
        hits_exp_2 = len(self.c.fetchall())
        tot_hits = hits_exp_0 + hits_exp_1 + hits_exp_2
        with self.conn:
            data = {'tothitsexp0': hits_exp_0,
                    'tothitsexp1': hits_exp_1,
                    'tothitsexp2': hits_exp_2,
                    'tothits': tot_hits,
                    'actor_id': actor_id}
            query = """UPDATE actors SET tothitsexp0 = :tothitsexp0, 
            tothitsexp1 = :tothitsexp1, tothitsexp2 = :tothitsexp2, tothits 
            = :tothits WHERE rowid = :actor_id LIMIT 1"""
            self.c.execute(query, data)
        print('db: updated total hits')

    def actor_finished(self, actor_id):
        timestamp = time.time()
        with self.conn:
            data = {'end': timestamp,
                    'endtxt': dt.datetime.fromtimestamp(timestamp)
                        .strftime('%Y-%m-%d %H:%M'),
                    'actor_id': actor_id}
            query = """UPDATE actors SET end={end},endtxt='{endtxt}' WHERE 
            rowid={actor_id}""".format(**data)
            self.c.execute(query)
            self.update_total_hits(actor_id)
        print('db: actor finished')

    def experiment_change(self, actor_id, experiment, change):
        experiment = int(experiment)
        timestamp = time.time()
        data = {'actor_id': actor_id, 'time': timestamp, 'exp': experiment}
        if change == 'start':
            with self.conn:
                self.c.execute(
                    """UPDATE actors SET startexp{exp}={time} 
                    WHERE rowid={actor_id} LIMIT 1""".format(**data),
                )
            print('db: experiment {} started'.format(experiment))
        elif change == 'end':
            with self.conn:
                self.c.execute(
                    """UPDATE actors SET endexp{exp}={time} 
                    WHERE rowid={actor_id} LIMIT 1""".format(**data),
                )
            print('db: experiment {} ended'.format(experiment))
        else:
            print('db: not able to process experiment change')

    def new_hit(self, actor_id, button, experiment):
        with self.conn:
            self.c.execute(
                """INSERT INTO hits VALUES (:actor_id, :experiment, :button, 
                :time)""",
                {'actor_id': actor_id,
                 'experiment': int(experiment),
                 'button': int(button),
                 'time': time.time()})
            # self.update_total_hits(actor_id)
        print('db: new hit registered for btn {}'.format(button))

    def all_actors_html(self):
        cols_head = ['ID', 'Nickname', 'Group', 'Age', 'Start', 'End',
                     'Start 0', 'End 0', 'Start 1', 'End 1', 'Start 2',
                     'End 2', 'Hits 0', 'Hits 1', 'Hits 2']
        cols = ['rowid', 'nickname', 'crowd', 'age', 'starttxt', 'endtxt',
                'startexp0', 'endexp0', 'startexp1', 'endexp1',
                'startexp2', 'endexp2', 'tothitsexp0', 'tothitsexp1',
                'tothitsexp2']
        self.c.execute("""SELECT {} FROM actors""".format(', '.join(cols)))
        table = '<table><tbody>'
        header = '<tr>{}</tr>'.format('<td>{}</td>' * len(cols))
        header = header.format(*cols_head)
        table += header
        for row in self.c.fetchall():
            table += '<tr>{}</tr>'.format(
                ('<td>{}</td>' * len(cols)).format(*row))
        table += '</tbody></table>'
        return self.table_base.format(style=self.table_style, table_html=table)

    def highscore_html(self):
        cols_head = ['Nickname', 'Group', 'Total hits']
        cols = ['nickname', 'crowd', 'tothits']
        self.c.execute("""SELECT {} FROM actors ORDER BY tothits DESC"""
                       .format(', '.join(cols)))
        table = '<table><tbody>'
        header = '<tr>{}</tr>'.format('<td>{}</td>' * len(cols))
        header = header.format(*cols_head)
        table += header
        for row in self.c.fetchall():
            table += '<tr>{}</tr>'.format(
                ('<td>{}</td>' * len(cols)).format(*row))
        table += '</tbody></table>'
        return self.table_base.format(style=self.table_style, table_html=table)


if __name__ == '__main__':
    choices = {'create': DB.createdb, 'check': DB.check}
    parser = argparse.ArgumentParser(
        description='Manage the database')
    parser.add_argument(
        'command',
        choices=choices,
        help='''the command you want to perform''')

    args = parser.parse_args()

    command = choices[args.command]
    command()

# -*- coding: utf-8 -*-
import argparse
import sqlite3
import time
from os import path
import datetime as dt


class DB:
    db_name = 'data.db'
    db_path = path.join(path.dirname(__file__), db_name)

    def __init__(self):
        if not path.isfile(self.db_path):
            self.createdb()

        self.conn = sqlite3.connect(self.db_path)
        # self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    @classmethod
    def check(cls):
        if path.isfile(cls.db_path):
            print('found file')
        else:
            print('did not find file')

    @classmethod
    def createdb(cls):
        if not path.isfile(cls.db_path):
            conn = sqlite3.connect(cls.db_path)
            # conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""CREATE TABLE actors (
                age integer,
                gender integer,
                game integer,
                start real,
                end real,
                crowd integer,
                startexp1 real,
                startexp2 real,
                endexp1 real,
                endexp2 real,
                tothitsexp1 integer,
                tothitsexp2 integer
                )""")
            c.execute("""CREATE TABLE hits (
                actor integer,
                button integer,
                time integer
                )""")
            conn.commit()
            conn.close()
            print('Created DB at {}'.format(cls.db_path))
        else:
            raise FileExistsError('{} already exist'.format(cls.db_path))

    def last_id(self):
        self.c.execute(
            """SELECT rowid FROM actors ORDER BY rowid DESC""")
        id_ = self.c.fetchone()[0]
        print('found id {}'.format(id_))
        return id_

    def new_actor(self, age, gender, game_consumption):
        with self.conn:
            self.c.execute(
                """INSERT INTO actors (age, gender, game, start) 
                VALUES (:age, :gender, :game, :start)""",
                {'age': int(age),
                 'gender': int(gender),
                 'game': int(game_consumption),
                 'start': time.time()})
        print('db: new actor created')

    def new_hit(self, actor, button):
        with self.conn:
            self.c.execute(
                """INSERT INTO hits VALUES (:actor, :button, :time)""",
                {'actor': actor,
                 'button': button,
                 'time': time.time()})
        print('db: new hit registered')

    def all_actors_html(self):
        cols_head = ['ID', 'Age', 'Game consumption', 'Start', 'End']
        cols = ['rowid', 'age', 'game', 'start', 'end']
        self.c.execute("""SELECT {} FROM actors""".format(', '.join(cols)))
        table = '<table><tbody>'
        header = '<tr><tr>'.format('<td>{}</td>'*len(cols))
        header.format(*cols_head,)
        for row in self.c.fetchall():
            id, age, game, start_stamp, end_stamp = row
            start = dt.datetime.fromtimestamp(
                int(start_stamp)).strftime('%Y-%m-%d %H:%M')
            if end_stamp:
                end = dt.datetime.fromtimestamp(
                    int(end_stamp)).strftime('%Y-%m-%d %H:%M')
            else:
                end = 'None'
            table += ('<td>{}</td>'*len(cols)).format(id, age, game, start, end)
        table += '</tbody></table>'
        return table

    def n_actors(self):
        self.c.execute("""SELECT rowid FROM actors""")
        return str(len(self.c.fetchall()))

    def actor(self, actor_id):
        self.c.execute(
            """SELECT * FROM actors WHERE rowid='{}'""".format(actor_id))
        text = str(self.c.fetchone())
        print(text)
        return text

    def get_hits(self, actor_id):
        self.c.execute(
            """SELECT * FROM hits WHERE actor='{}'""".format(actor_id))
        return self.c.fetchall()

    def add_column(self, table, column, type_, default):
        with self.conn:
            self.c.execute("ALTER TABLE {} ADD COLUMN '{}' '{}' DEFAULT {}"
                           .format(table, column, type_, default))

    def clear_table(self, table):
        with self.conn:
            self.c.execute("DELETE FROM {}".format(table))


if __name__ == '__main__':
    choices = {'createdb': DB.createdb, 'check': DB.check}
    parser = argparse.ArgumentParser(
        description='Start a streaming video server on raspberry pi')
    parser.add_argument(
        'command',
        choices=choices,
        help='''the command you want to perform''')

    args = parser.parse_args()

    command = choices[args.command]
    command()

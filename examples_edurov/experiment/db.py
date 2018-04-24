# -*- coding: utf-8 -*-
import argparse
import sqlite3
import time
from os import path


class DB:
    db_name = 'data.db'
    db_path = path.join(path.dirname(__file__), db_name)

    def __init__(self):
        if not path.isfile(self.db_path):
            self.createdb()

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
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
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""CREATE TABLE actors (
                age integer,
                gender integer,
                game integer,
                start real,
                end real DEFAULT 0,
                crowd integer DEFAULT 0,
                startexp1 real DEFAULT 0,
                startexp2 real DEFAULT 0,
                endexp1 real DEFAULT 0,
                endexp2 real DEFAULT 0,
                tothitsexp1 integer DEFAULT 0,
                tothitsexp2 integer DEFAULT 0
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

    @classmethod
    def load(cls, db):
        return cls(db=db)

    def new_actor(self, age, gender, game_consumption):
        with self.conn:
            self.c.execute(
                """INSERT INTO actors VALUES (:age, :gender, :game, :start)""",
                {'age': age,
                 'gender': gender,
                 'game': game_consumption,
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

    def n_actors(self):
        self.c.execute("""SELECT rowid FROM actors""")
        print('{} participants in the experiment so far'
              .format(self.c.fetchall()))

    def clear_table(self, table):
        with self.conn:
            self.c.execute("DELETE FROM {}".format(table))

    def print_actor(self, actor_id):
        self.c.execute(
            """SELECT * FROM actors WHERE rowid='{}'""".format(actor_id))
        print(self.c.fetchone())

    def get_hits(self, actor_id):
        self.c.execute(
            """SELECT * FROM hits WHERE actor='{}'""".format(actor_id))
        return self.c.fetchall()

    def add_column(self, table, column, type_, default):
        with self.conn:
            self.c.execute("ALTER TABLE {} ADD COLUMN '{}' '{}' DEFAULT {}"
                           .format(table, column, type_, default))


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

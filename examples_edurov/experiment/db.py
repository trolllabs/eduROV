# -*- coding: utf-8 -*-
import os.path
import sqlite3
import time
from os import path


class DB:
    db_name = 'data.db'
    db_path = path.join(path.dirname(__file__), db_name)

    def __init__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

        if not path.isfile(self.db_path):
            self.new_database()

    def new_database(self):
        if not os.path.isfile(self.db_path):
            self.c.execute("""CREATE TABLE actors (
                age integer,
                gender integer,
                game integer,
                start real,
                end real,
                order integer,
                startexp1 real,
                startexp2 real,
                endexp1 real,
                endexp2 real,
                tothitsexp1 integer,
                tothitsexp2 integer,
                )""")
            self.c.execute("""CREATE TABLE hits (
                actor integer,
                button integer,
                time integer,
                )""")
            self.conn.commit()
            print('Database created')
        else:
            raise FileExistsError('{} already exist'.format(self.db_name))

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

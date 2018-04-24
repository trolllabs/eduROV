# -*- coding: utf-8 -*-
import argparse
import datetime as dt
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
            c = conn.cursor()
            c.execute("""CREATE TABLE actors (
                nickname text, 
                age integer,
                gender integer,
                game integer,
                start real,
                starttxt text,
                end real,
                endtxt text,
                crowd integer,
                startexp1 real,
                startexp2 real,
                endexp1 real,
                endexp2 real,
                tothitsexp1 integer,
                tothitsexp2 integer,
                tothits integer,
                valid integer
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
        self.c.execute("""SELECT rowid FROM actors ORDER BY rowid DESC""")
        id_ = self.c.fetchone()[0]
        print('found id {}'.format(id_))
        return id_

    def next_crowd(self):
        with self.conn:
            self.c.execute("""SELECT rowid FROM actors WHERE crowd='0'""")
            crowd_0 = len(self.c.fetchall())
            self.c.execute("""SELECT rowid FROM actors WHERE crowd='1'""")
            crowd_1 = len(self.c.fetchall())
        if crowd_0 > crowd_1:
            return 1
        else:
            return 0


    def new_actor(self, nickname, age, gender, game_consumption):
        timestamp = time.time()
        with self.conn:
            self.c.execute(
                """INSERT INTO actors (nickname, age, gender, game, start, starttxt, crowd) 
                VALUES (:nickname, :age, :gender, :game, :start, :starttxt, :crowd)""",
                {'nickname': nickname,
                 'age': int(age),
                 'gender': int(gender),
                 'game': int(game_consumption),
                 'start': timestamp,
                 'starttxt': dt.datetime.fromtimestamp(timestamp).strftime(
                     '%Y-%m-%d %H:%M'),
                 'crowd':self.next_crowd()})
        print('db: new actor created')

    def new_hit(self, actor_id, button):
        with self.conn:
            self.c.execute(
                """INSERT INTO hits VALUES (:actor_id, :button, :time)""",
                {'actor_id': actor_id,
                 'button': button,
                 'time': time.time()})
        print('db: new hit registered')

    def all_actors_html(self):
        cols_head = ['ID', 'Nickname', 'Group', 'Age', 'Game consumption', 'Start', 'End']
        cols = ['rowid', 'nickname', 'crowd', 'age', 'game', 'starttxt', 'endtxt']
        self.c.execute("""SELECT {} FROM actors""".format(', '.join(cols)))
        table = '<table><tbody>'
        header = '<tr>{}</tr>'.format('<td>{}</td>' * len(cols))
        header = header.format(*cols_head)
        table += header
        for row in self.c.fetchall():
            table += '<tr>{}</tr>'.format(
                ('<td>{}</td>' * len(cols)).format(*row))
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

    def clear_table(self, table):
        with self.conn:
            self.c.execute("DELETE FROM {}".format(table))

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
        return table


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

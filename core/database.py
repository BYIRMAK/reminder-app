# Database module implementation with SQLite

import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        """ create a database connection to a SQLite database """
        self.connection = self.create_connection(db_file)
        self.create_table()

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        """ create the reminders table """
        create_table_sql = '''CREATE TABLE IF NOT EXISTS reminders (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    description text,
                                    datetime text NOT NULL,
                                    category text,
                                    tags text,
                                    repeat text,
                                    priority text,
                                    active boolean NOT NULL
                                );''' 
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def add_reminder(self, title, description, datetime, category, tags, repeat, priority, active):
        """ add a new reminder to the reminders table """
        sql = ''' INSERT INTO reminders(title, description, datetime, category, tags, repeat, priority, active)
                  VALUES(?,?,?,?,?,?,?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, (title, description, datetime, category, tags, repeat, priority, active))
        self.connection.commit()
        return cur.lastrowid

    # other methods for getting, updating, and deleting reminders...
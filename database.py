import sqlite3
import datetime

class DB:
    def __init__(self, dbname='data.sqlite3'):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS Materials (
            material_id INTEGER NOT NULL UNIQUE,
            name VARCHAR(50) NOT NULL,

            PRIMARY KEY(material_id AUTOINCREMENT)
        );
        
        CREATE TABLE IF NOT EXISTS Prices (
            price_id INTEGER NOT NULL UNIQUE,
            material_id INTEGER NOT NULL,
            date INTEGER,
            price INTEGER,

            FOREIGN KEY(material_id) REFERENCES Materials(material_id),
            PRIMARY KEY(price_id AUTOINCREMENT)
        );

        ''')
    def get_material_id(self, name):
        # gets the name of a material and returns its id in database
        # returns none if not found in database
        self.cur.execute('SELECT material_id FROM materials WHERE name=?', (name, ))
        row = self.cur.fetchone()
        return None if row is None else row[0]

a = DB()
a.get_material_id('test')
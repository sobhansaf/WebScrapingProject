import sqlite3
import datetime

class DB:
    def __init__(self, dbname='data.sqlite3'):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS Materials (
            material_id INTEGER NOT NULL UNIQUE,
            name VARCHAR(50),

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



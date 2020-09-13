import sqlite3
import datetime

class DB:

    def __init__(self, dbname='data.sqlite3'):
        self.total_materials = 0
        self.total_prices = 0
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS Materials (
            material_id INTEGER NOT NULL UNIQUE,
            name VARCHAR(50) NOT NULL UNIQUE,

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

    def add_material(self, name):
        # adds a new material in database if it doesn't exists, returns its material_id.
        if not self.get_material({'name': name}):
            self.cur.execute('INSERT INTO Materials(name) VALUES (?)', (name, ))
            self.total_materials += 1   

            if self.total_materials % 10 == 0: 
                # for better perfomance, each 10 new material added to db one commit will be performed,
                self.conn.commit()

        return self.get_material({'name': name})[0]

    def get_material(self, info={}):
        # gets the info of a material and returns its id in database
        # info is a dict, containing infromation of a record -> info = {'name': 'gold'} , info = {'material_id': 24} , info={}
        # returns all of the materials if info is an empty dict
        # returns none if not found in database
        if type(info) != dict:
            raise TypeError('info argument must be a dict!')

        sql = 'SELECT material_id, name FROM materials WHERE '
        values = list()
        
        for key in info:
            sql += f'{key.lower()}=? AND '
            values.append(info[key])
        
        if sql.endswith('AND '):
            # in each iteration of for loop above, an "AND" is added at the end of sql, removing that "AND"
            sql = sql[:-5] 
        else:
            # info was empty, returning all of the materials, removing last "WHERE" from sql statement
            sql = sql[:-7]

        self.cur.execute(sql, values)
        return self.cur.fetchall()

    def __del__(self):
        print('finishing ...')
        self.conn.commit()
        self.conn.close()


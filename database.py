import sqlite3
import datetime
import material
import price

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

    def _make_where_clouse_to_insert(self, info, sql):
        # makes a where clouse according to info and sql. info is a dict and sql is a string
        # e.g: info={'name': 'mat'}, sql='SELECT * FROM MATERIAL' 
        # --> return: ("SELECT * FROM MATERIAL WHERE name=?", [mat])
        if type(info) != dict or type(sql) != str:
            raise TypeError('info argument must be a dict and sql must be a string!')

        if not sql.lower().strip().endswith('where'):
            sql += ' WHERE '
        
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
        
        return sql, values


    def add_material(self, name):
        # adds a new material in database if it doesn't exists, returns its material_id.
        if not self.get_material({'name': name}):
            self.cur.execute('INSERT INTO Materials(name) VALUES (?)', (name, ))
            self.total_materials += 1   

            if self.total_materials % 10 == 0: 
                # for better perfomance, each 10 new material added to db one commit will be performed,
                self.conn.commit()

        return self.get_material({'name': name})[0].id

    def get_material(self, info={}):
        # gets the info of a material and returns its id in database
        # info is a dict, containing infromation of a record -> info = {'name': 'gold'} , info = {'material_id': 24} , info={}
        # returns a list of materials in form of some material objects
        # returns all of the materials if info is an empty dict
        # returns none if not found in database
        if type(info) != dict:
            raise TypeError('info argument must be a dict!')

        # making a select statement according to info. sql will be something like: SELECT ... FROM ... WHERE name=?
        # values is a list of corresponding "?" of sql
        sql, values = self._make_where_clouse_to_insert(info, 'SELECT material_id, name FROM materials WHERE ')

        self.cur.execute(sql, values)
        fetched = list(self.cur.fetchall())

        for i in range(len(fetched)):
            fetched[i] = material.material(*fetched[i])
        
        return fetched

    def add_price(self, material_name, date, price):
        # gets price info and adds a new price record in table:
        material = self.get_material({'name': material_name})
        if not material:
            material_id = self.add_material(material_name)
        else:
            material_id = material[0].id

        # prventing duplication
        prices = self.get_price({'material_id': material_id})
        if prices:
            # price exists in db
            for price_ in prices:
                if (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds() - price_.date < 2 * 3600: 
                    # last update was less than 2 hours before
                    return price_.id
        
        sql = 'INSERT INTO Prices(material_id, date, price) VALUES (?, ?, ?)'
        self.cur.execute(sql, (material_id, date, price))

        self.total_prices += 1
        if self.total_prices % 10 == 0:
            self.conn.commit()

        return self.get_price({'material_id': material_id, 'date': int(date), 'price': int(price)})[0].id


    def get_price(self, info):
        if type(info) != dict:
            raise TypeError('info must be a dict!')

        # making a select statement according to info. sql will be something like: SELECT ... FROM ... WHERE name=?
        # values is a list of corresponding "?" of sql
        sql, values = self._make_where_clouse_to_insert(info, 'SELECT price_id, material_id, price, date FROM Prices')

        self.cur.execute(sql, values)
        fetched = list(self.cur.fetchall())

        for i in range(len(fetched)):
            fetched[i] = price.price(*fetched[i])
        
        return fetched

        

    def __del__(self):
        self.conn.commit()
        self.conn.close()



import mysql.connector as mysql
from geopy.geocoders import Nominatim
from datetime import datetime
"""
sql cursor docs
https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html


"""


class Connection:

    def __init__(self, config=None):
        if config is None:
            config = {
                "user": "root",
                "password": "password",
                "host": "localhost",
                "database": "databases7"
            }
        self.conn = mysql.connect(**config)
        # self.conn = conn
        self.cursor = self.conn.cursor()
        self.geolocator = None
        self.user = 'Stan'
        self.isVolunteer = True
        self.isAdmin = True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.close()

    def execute(self, *args, **kwargs):
        self.cursor.execute(*args, **kwargs)

    def executemany(self, operation, param_sequence):
        '''Like execute, but repeats the operation with different parameters'''
        self.cursor.executemany(operation, param_sequence)

    def fetch(self, count=None):
        if count is None:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(size=count)

    def exec_proc(self, procedure, *params):
        '''Use to execute a stored procedure with no results'''
        self.cursor.callproc(procedure, *params)

    def single_proc(self, procedure, *params):
        '''Use to get the result of stored procedures with a single result'''
        self.cursor.callproc(procedure, *params)
        result = next(self.cursor.stored_results())
        return result.fetchall()

    def commit(self, *args, **kwargs):
        self.conn.commit(*args, **kwargs)

    def close(self, commit=False):
        if commit:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_tables(self):
        self.execute("SHOW TABLES")
        return self.fetch()

    def check_location(self, location):
        geolocator = Nominatim(user_agent="DatabaseProject7")
        loc = geolocator.geocode(location)
        return loc

    # Disasters Methods
    def insert_disaster(self, location, radius, name, description, date=datetime.now().date(), commit=True):
        if self.geolocator is None:
            self.geolocator = Nominatim(user_agent="DatabaseProject7")
        loc = self.geolocator.geocode(location)
        if loc is None:
            return False
        lat, long = loc.latitude, loc.longitude
        op = ("INSERT INTO Disasters (DisasterLocation, Latitude, Longitude, Radius, Name, Description, StartDate) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        data = (location, lat, long, radius, name, description, date)
        self.execute(op, data)
        self.commit()

    def end_disaster(self, disaster_ID, commit=True):
        self.exec_proc('end_disaster', [disaster_ID])
        if commit:
            self.commit()

    def select_disaster(self, disaster_id):
        return self.single_proc('select_disaster', [disaster_id])

    def short_disasters(self, activeOnly=False):
        return self.single_proc('short_disasters', [1 if activeOnly else 0])

    # Goods Methods
    def select_goods(self):
        return self.single_proc('select_goods')

    def search_goods(self, searchTerm):
        return self.single_proc('search_goods', [searchTerm + '%'])

    def select_goods_categories(self):
        return self.single_proc('goods_categories')

    def insert_good(self, name, category, unitOfMeasure):
        op = ("INSERT INTO PossibleGoods (Category, Name, UnitOfMeasure) VALUES (%s %s %s)")
        data = (category, name, unitOfMeasure)
        self.execute(op, data)
        self.commit()

    # Requests Methods
    def insert_request(self, user, disaster, good, duration, quantity):
        date = datetime.new().date()
        op = ("INSERT INTO Requests (UserID, DisasterID, GoodsID, DatePosted, Duration, QuantityNeeded, QuantityReceived) VALUES (%s %s %s %s %s %s %s)")
        data = (user, disaster, good, date, duration, quantity, 0)
        self.execute(op, data)
        self.commit()


if __name__ == '__main__':
    # print(check_location("Iowa City").json)
    with Connection() as conn:
        print(conn.search_goods("App"))

import mysql.connector as mysql
from geopy.geocoders import Nominatim
from datetime import datetime
"""
sql cursor docs
https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html


"""


class Connection:

    def __init__(self):
        _config = {
            "user": "root",
            "password": "password",
            "host": "localhost",
            "database": "databases7"
        }
        self.conn = mysql.connect(**_config)
        self.cursor = self.conn.cursor()
        self.geolocator = None

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

    def insert_disaster(self, location, radius, name, description, date=datetime.now().date(), commit=True):
        disaster_ID = self.next_disaster_id()
        if self.geolocator is None:
            self.geolocator = Nominatim(user_agent="DatabaseProject7")
        loc = self.geolocator.geocode(location)
        if loc is None:
            return False
        lat, long = loc.latitude, loc.longitude
        op = ("INSERT INTO Disasters (DisasterID, DisasterLocation, Latitude, Longitude, Radius, Name, Description, StartDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        data = (disaster_ID, location, lat, long, radius, name, description, date)
        self.execute(op, data)
        self.commit()

    def next_disaster_id(self):
        prevID = self.single_proc('next_disaster_id')
        if len(prevID) == 0:
            nextID = 1
        else:
            nextID = prevID[0][0] + 1
        return nextID

    def end_disaster(self, disaster_ID, commit=True):
        self.exec_proc('end_disaster', [disaster_ID])
        if commit:
            self.commit()

    def select_disaster(self, disaster_id):
        return self.single_proc('select_disaster', [disaster_id])

    def short_disasters(self, onlyActive=False):
        return self.single_proc('short_disasters', [1 if onlyActive else 0])

    def select_goods(self):
        return self.single_proc('select_goods')


def check_location(location):
    geolocator = Nominatim(user_agent="DatabaseProject7")
    loc = geolocator.geocode(location)
    return loc


if __name__ == '__main__':
    # print(check_location("Iowa City").json)
    with Connection() as conn:
        print(conn.select_disaster(2))
        conn.end_disaster(2)
        print(conn.select_disaster(2))

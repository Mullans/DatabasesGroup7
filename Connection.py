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
        """Like execute, but repeats the operation with different parameters"""
        self.cursor.executemany(operation, param_sequence)

    def fetch(self, count=None):
        if count is None:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(size=count)

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
        op = "SELECT DisasterID FROM Disasters ORDER BY DisasterID DESC LIMIT 1"
        self.execute(op)
        prevID = self.fetch()
        if len(prevID) == 0:
            nextID = 1
        else:
            nextID = prevID[0][0] + 1
        print(prevID)
        print(nextID)
        return nextID

    def end_disaster(self, disaster_ID, commit=True):
        op = "UPDATE Disasters SET Active = 0 WHERE DisasterID = %s"
        data = (disaster_ID,)
        self.execute(op, data)
        self.commit()

    def select_disasters(self, conditions=None, activeOnly=False, orderBy=None, shortForm=False):
        query = "SELECT DisasterID, Name, DisasterLocation, StartDate, Active FROM Disasters" if shortForm else "SELECT * FROM Disasters"
        if activeOnly:
            if conditions is None:
                conditions = []
            conditions.append('Active = 1')
        if conditions is not None:
            if type(conditions) == list:
                conditions = ['(' + item + ')' for item in conditions]
                conditions = " AND ".join(conditions)
            query += " WHERE " + conditions
        if orderBy is not None:
            query += " ORDER BY " + orderBy
        self.execute(query)
        return self.fetch()


def check_location(location):
    geolocator = Nominatim(user_agent="DatabaseProject7")
    loc = geolocator.geocode(location)
    return loc

if __name__ == '__main__':
    # print(check_location("Iowa City").json)
    datetime

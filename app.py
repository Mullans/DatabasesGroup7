from flask import Flask, render_template, request, abort
from Connection import Connection, check_location
import json
from datetime import datetime
import mysql.connector as mysql

app = Flask(__name__)


@app.route('/')
def index():
    return ""


@app.route('/disasters')
def disasters():
    with Connection() as conn:
        conn.next_disaster_id()
        disasters = conn.select_disasters(orderBy='DisasterID', shortForm=True)
    return render_template('./disasters.html', name='tester', today=datetime.now().date().strftime("%m/%d/%Y"), disasters=disasters)


@app.route('/disaster_<disasterID>')
def disaster_item(disasterID):
    with Connection() as conn:
        disaster = conn.select_disasters(conditions="DisasterID={}".format(disasterID))
        if len(disaster) == 0:
            abort(404)
        disaster = list(disaster[0])
        disaster[7] = disaster[7].strftime('%b %d, %Y')
    return render_template("disaster_template.html", disaster=disaster)


@app.route('/disaster_<disasterID>_deactivate')
def deactivate_disaster(disasterID):
    print("Deactivating {}".format(disasterID))
    try:
        with Connection() as conn:
            conn.end_disaster(disasterID)
        return '{"message": "Success"}'
    except Exception as e:
        print(e)
        return '{"message": "Falure"}'


@app.route('/createDisaster', methods=['POST', 'GET'])
def create_disaster():
    if request.method == 'POST':
        result = request.form
        valid_location = check_location(result['DisasterLocation']) is not None
        valid_name = len(result['DisasterName']) > 0
        valid_date = len(result['DisasterDate']) > 0
        date = datetime.strptime(result['DisasterDate'], '%m/%d/%Y') if valid_date else None
        if valid_location and valid_name:
            with Connection() as conn:
                try:
                    conn.insert_disaster(result['DisasterLocation'], result['DisasterRadius'], result['DisasterName'], result['DisasterDescription'], date=date)
                    success = True
                except Exception as e:
                    print(e)
                    success = False
        else:
            success = False
        response = {
            "location": valid_location,
            "name": valid_name,
            "created": success
        }
        return json.dumps(response)
    else:
        abort(404)


@app.route('/createRequest')
def create_request_page():
    with Connection() as conn:
        disasters = conn.short_disasters(activeOnly=True)
    return render_template("makeRequest.html", disasters=disasters)


@app.route('/createRequest_new', methods=['POST', 'GET'])
def create_request():
    if request.method == 'POST':
        result = request.form
        return result
    else:
        abort(404)


"""JJ's Section START"""
dbConfig = {
            "user": "root",
            "password":"password",
            "host":"127.0.0.1",
            "database": "databases7"
            }
conn = mysql.connect(**dbConfig)

cursor = conn.cursor()


@app.route("/DisasterSearch")
def disaster_search_page():
    return render_template('DisasterSearch.html', posts = disaster_search())


def disaster_search():
    cursor.execute("SELECT * FROM Disasters")
    return cursor.fetchall()


@app.route("/UserSearch")
def user_search_page():
    return render_template('UserSearch.html',post = user_search())


def user_search():
    cursor.execute("SELECT * FROM User")
    return cursor.fetchall()

"""JJ's Section END"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

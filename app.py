from flask import Flask, render_template, request, abort
from Connection import Connection
import json
from datetime import datetime

app = Flask(__name__)

conn = Connection()


@app.route('/')
def index():
    return ""


@app.route('/admin_page')
def disasters():
    if not conn.isAdmin:
        abort(403)
    disasters = conn.short_disasters()
    return render_template('./admin_page.html', name='tester', today=datetime.now().date().strftime("%m/%d/%Y"), disasters=disasters)


@app.route('/disaster/<disasterID>')
def disaster_item(disasterID):
    disaster = conn.select_disaster(disasterID)
    if len(disaster) == 0:
        abort(404)
    disaster = list(disaster[0])
    disaster[7] = disaster[7].strftime('%b %d, %Y')
    return render_template("disaster_template.html", disaster=disaster)


# TODO: Change this from JSON to POST
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


@app.route('/createDisaster', methods=['POST'])
def create_disaster():
    if request.method == 'POST':
        result = request.form
        valid_location = conn.check_location(result['DisasterLocation']) is not None
        valid_name = len(result['DisasterName']) > 0
        valid_date = len(result['DisasterDate']) > 0
        date = datetime.strptime(result['DisasterDate'], '%m/%d/%Y') if valid_date else None
        if valid_location and valid_name:
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


@app.route('/disaster/<disasterID>/newRequest')
def create_request_page(disasterID):
    disaster = conn.select_disaster(disasterID)
    if len(disaster) == 0:
        abort(404)
    disaster = list(disaster[0])
    return render_template("makeRequest.html", disaster=disaster)


@app.route('/searchGoods/<searchTerm>')
def search_goods(searchTerm):
    goods = conn.search_goods(searchTerm)
    response = {"result": goods}
    return json.dumps(response)


@app.route('/createRequest', methods=['POST'])
def create_request():
    if request.method == 'POST':
        result = request.form
        print(result)
        return "It works?"
    else:
        abort(404)


"""JJ's Section START"""
import mysql.connector as mysql

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

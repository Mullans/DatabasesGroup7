from flask import Flask, render_template
import mysql.connector as mysql
app = Flask(__name__)



dbConfig = {
            "user": "root",
            "password":"password",
            "host":"127.0.0.1"
            }
conn = mysql.connect(**dbConfig)
#print(conn)
cursor = conn.cursor()

@app.route("/DisasterSearch")
def disaster_search():
    return render_template('DisasterSearch.html' , post = search())

def search():
    cursor.execute("SELECT * FROM Disaster")
    return cursor.fetchall()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

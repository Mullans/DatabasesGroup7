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
cursor1 = conn.cursor()
cursor1.execute("USE database3")

@app.route("/DisasterSearch")
def user_search():
    return render_template('DIsasterSearch.html' , post = search.posts)

def search():
    cursor = conn.cursor()
    posts =[ cursor.execute("SELECT * FROM Disaster")]
    return (cursor.fetchall())
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
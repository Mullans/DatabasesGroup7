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
cursor.execute("USE database7")

@app.route("/UserSearch")
def user_search():
    return render_template('UserSearch.html',post = search.post)

def search():
    
    post =[ cursor.execute("SELECT * FROM User")]
    return (cursor.fetch())
    
if __name__ == '__main__':
    app.run(debug=True)    
from flask import Flask, render_template, request, abort, flash, redirect, url_for, session
import json
from datetime import datetime
from passlib.hash import sha256_crypt
# from flask_login import current_user, login_user, logout_user
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, validators

from Connection import Connection

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'  # '961216'
app.config['MYSQL_DATABASE_DB'] = 'databases7'  # 'myapp'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'  # 'db4free.net'
app.secret_key = '123'
mysql.init_app(app)
conn = Connection(mysql.connect())


@app.route('/')
def index():
    return ""


'''Sean's Section START'''


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


'''Sean's Section END'''


"""JJ's Section START"""


@app.route("/DisasterSearch")
def disaster_search_page():
    return render_template('DisasterSearch.html', posts=disaster_search())


def disaster_search():
    conn.execute("SELECT * FROM Disasters")
    return conn.fetch()


@app.route("/UserSearch")
def user_search_page():
    return render_template('UserSearch.html', post=user_search())


def user_search():
    conn.execute("SELECT * FROM User")
    return conn.fetch()



@app.route("/Email_Confirm/<username>")
def email_confirm(UserId):
    conn.execute("SELECT email FROM User WHERE username = " + UserId)
    email = conn.fetch()
    conn.execute("SELECT first_name FROM User WHERE username = " + UserId)
    first_name = conn.fetch()
    conn.execute("SELECT last_name FROM User WHERE username = " + UserId)
    last_name = conn.fetch()
    name = first_name +" " + last_name
    
    requests.post(
            "https://api.mailgun.net/v3/sandbox93a72ba2ea354d68a0ee1eda24aab168.mailgun.org/messages",
        auth=("api", "api code goes here"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox93a72ba2ea354d68a0ee1eda24aab168.mailgun.org>",
              "to":  email,
              "subject": "Hello  "+ name,
              "text": "Congratulations "+ first_name + ", you just confirmed your email!"})
    
    return redirect(url_for('email'))

"""JJ's Section END"""


'''Amy's section START'''


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password_candidate = request.form['password_']  # password
        cursor = conn.cursor
        name = cursor.execute("select * from Users where username= %s", request.form['username'])
        app.secret_key = '123'
        session['username'] = request.form['username']
        if name > 0:
            data = cursor.fetchone()  # fetchall

            password_ = data[4]  # tuple
            if sha256_crypt.verify(password_candidate, password_):
                flash('You have successfully logged in!', 'success')
                return render_template('login.html')  # ,UserID=username) #return redirect(url_for('profile'),username))

            else:
                flash('Error: Password is incorrect! Please try again!', 'error')
        else:
            flash("Error: Username does not exist! Please try again!", 'error')
    return render_template('login.html')


@app.route('/profile/<string:username>/')
def profile(username):
    # con=mysql.connect()
    cursor = conn.cursor
    cursor.execute("select * from Users where username=%s", [username])
    user = cursor.fetchone()
    return render_template('profile2.html', user=user)


@app.route('/profile/<string:username>/edit')
def edit_Profile(username):
    cursor = conn.cursor
    cursor.execute("select* from Users where username=%s", [username])
    user = cursor.fetchone()
    return render_template('edit.html', user=user)


class UserRegister(Form):
    first_name = StringField('First Name', validators=[validators.input_required()])
    last_name = StringField('Last Name', validators=[validators.input_required()])
    phone = StringField('Phone Number', validators=[validators.input_required()])
    email = StringField('Email Address', validators=[validators.input_required()])
    address = StringField('Home Address', validators=[validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password_ = PasswordField('Password', validators=[validators.input_required(), validators.EqualTo('checkPassword', message='Passwords do not match!')])
    checkPassword = PasswordField('Enter Password Again')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = UserRegister(request.form)
    if request.method == 'POST' and form.validate():
        u = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'address': form.address.data,
            'username': form.username.data,
            'password_': sha256_crypt.encrypt(str(form.password_.data)),
            'phone': form.phone.data
        }
        cursor = conn.cursor
        loc = conn.check_location(u['address'])
        u['lat'], u['long'] = loc.latitude, loc.longitude
        print(u['lat'], u['long'])
        query = "insert into Users (last_name, first_name, username, password_, email, address, phone, latitude, longitude) values(%(last_name)s, %(first_name)s, %(username)s, %(password_)s, %(email)s,%(address)s, %(phone)s, %(lat)s, %(long)s)"

        cursor.execute(query, u)

        """
        first_name=form.first_name.data
        last_name=form.last_name.data
        email=form.email.data
        address=form.address.data
        UserID=form.username.data
        password_=sha256_crypt.encrypt(str(form.password_.data))
        phone=form.phone.data
        con=mysql.connect()
        cursor=con.cursor()
        #cursor = mysql.get_db().cursor()
        cursor.execute("insert into user(last_name,first_name,username,password_,email,address,phone) values(%s,%s,%s,%s,%s,%s,%s) ",(first_name,last_name,username,password_,email,address,phone))
        """
        # data = cursor.fetchone()
        conn.commit()
        cursor.close()
        flash('Registration successful! Please check your email.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


'''Amy's section END'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

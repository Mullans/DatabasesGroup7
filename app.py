from flask import Flask, render_template, request, abort, flash, redirect, url_for, session
import json
from datetime import datetime
from passlib.hash import sha256_crypt
# from flask_login import current_user, login_user, logout_user
# from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, validators
from flask_mail import Mail, Message  # A
from itsdangerous import URLSafeTimedSerializer, SignatureExpired  # A

from Connection import Connection

app = Flask(__name__)
# mysql = MySQL()
app.config.from_pyfile('config.cfg')  # A

config = {
    "user": "root",
    "password": "Gsj123@#",  # '961216'
    "host": "localhost",  # 'db4free.net'
    "database": "project"  # 'myapp'
}
config=None
app.secret_key = '123'
conn = Connection(config=config)


# @app.route('/')
# def index():
#     return ""
# email confir
mail = Mail(app)
k = URLSafeTimedSerializer("123")
@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'GET':

        return render_template('email.html')

    email = request.form['email']
    token = k.dumps(email, salt='email-confirm')
    notice = Message('Confirm Email', sender='yuaimeee@gmail.com', recipients=[email])
    notice.body = 'Here is the link {}'.format(url_for('getconfirm', token=token, _external=True))
    mail.send(notice)
    flash('Confirmation email sent! Please check your email.','success')
    return render_template('email.html')
#email confir
@app.route('/email/<token>')
def getconfirm(token):
    try:
         email = k.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
         return '<h3>The token does not work anymore</h3>'
    return '<h3>The token works</h3>'


'''Sean's Section START'''


@app.route('/admin_page')
def admin_page():
    if not conn.isAdmin:
        return redirect(url_for('disasters'))
    disasters = conn.short_disasters()
    return render_template('./admin_page.html', name='tester', today=datetime.now().date().strftime("%m/%d/%Y"), disasters=disasters)


@app.route('/disasters')
def disasters():
    disasters = conn.short_disasters()
    return render_template('./disasters.html', disasters=disasters)


@app.route('/disaster/<disasterID>')
def disaster_item(disasterID):
    disaster = conn.select_disaster(disasterID)
    print(disaster)
    if len(disaster) == 0:
        abort(404)
    disaster = list(disaster[0])
    disaster[7] = disaster[7].strftime('%b %d, %Y')
    return render_template("disaster_template.html", disaster=disaster, admin=conn.isAdmin)


# TODO: Change this from JSON to POST
@app.route('/disaster_<disasterID>_deactivate')
def deactivate_disaster(disasterID):
    print("Deactivating {}".format(disasterID))
    try:
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


@app.route('/disaster/<disasterID>/newOffer')
def create_offer_page(disasterID):
    disaster = conn.select_disaster(disasterID)
    if len(disaster) == 0:
        abort(404)
    disaster = list(disaster[0])
    return render_template("makeOffer.html", disaster=disaster)


@app.route('/disaster/<disasterID>/volunteer')
def volunteer_page(disasterID):
    disaster = conn.select_disaster(disasterID)

    if len(disaster) == 0:
        abort(404)
    disaster = list(disaster[0])
    return render_template("newVolunteer.html", disaster=disaster)


@app.route('/searchGoods/<searchTerm>')
def search_goods(searchTerm):
    goods = conn.search_goods(searchTerm)
    response = {"result": goods}
    return json.dumps(response)


@app.route('/createRequest/<disasterID>', methods=['POST'])
def create_request(disasterID):
    if request.method == 'POST':
        result = request.form
        items = []
        result_dict = json.loads(next(result.items())[0])
        for item in result_dict.items():
            items.append([item[1][0][0], item[1][1], item[1][2]])
        try:
            conn.insert_requests(conn.user, disasterID, items)
            return json.dumps({"result": True})
        except Exception as e:
            return json.dumps({"result": False})
    else:
        abort(404)


@app.route('/createOffer/<disasterID>', methods=['POST'])
def create_offer(disasterID):
    if request.method == 'POST':
        result = request.form
        items = []
        result_dict = json.loads(next(result.items())[0])
        for item in result_dict.items():
            items.append([item[1][0][0], item[1][1], item[1][2]])
        try:
            conn.insert_offers(conn.user, disasterID, items)
            return json.dumps({"result": True})
        except Exception as e:
            return json.dumps({"result": False})
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
    name = first_name + " " + last_name

    requests.post(
            "https://api.mailgun.net/v3/sandbox93a72ba2ea354d68a0ee1eda24aab168.mailgun.org/messages",
        auth=("api", "api code goes here"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox93a72ba2ea354d68a0ee1eda24aab168.mailgun.org>",
              "to":  email,
              "subject": "Hello  " + name,
              "text": "Congratulations " + first_name + ", you just confirmed your email!"})

    return redirect(url_for('email'))

"""JJ's Section END"""

"""Gaurav's Section START"""

@app.route("/")
def dashboard_page():
    return render_template('dashboard.html', posts=dashboard_output(), posts2 = dashboard_output2(), posts3 = dashboard_output3())

def dashboard_output():
    conn.execute("SELECT r.RequestID, g.Name, g.Category, g.UnitOfMeasure, r.DatePosted, r.Duration, r.QuantityNeeded, r.QuantityReceived FROM Requests r , PossibleGoods g WHERE r.GoodsID = g.GoodsID ")
    data = conn.fetch()
    return data
def dashboard_output2():
    conn.execute("SELECT o.OfferID, g.Name, g.Category, g.UnitOfMeasure, o.DatePosted, o.Duration, o.QuantityOffered, o.QuantityClaimed FROM Offers o , PossibleGoods g WHERE o.GoodsID = g.GoodsID ")
    data2 = conn.fetch()
    return data2
def dashboard_output3():
    conn.execute("SELECT RequestID, PeopleNeeded, PeopleFound, WorkCategory FROM VolunteerRequests")
    data3 = conn.fetch()
    return data3

"""Gaurav's Section END"""


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

            password_ = data[3]  # tuple
            if sha256_crypt.verify(password_candidate, password_):
                flash('You have successfully logged in!', 'success')
                return render_template('login.html')  # ,UserID=username) #return redirect(url_for('profile'),username))

            else:
                flash('Error: Password is incorrect! Please try again!', 'error')
        else:
            flash("Error: Username does not exist! Please try again!", 'error')
    return render_template('login.html')

@app.route('/profile/<string:username>/')
def Create_profile(username):
    con=mysql.connect()
    cursor=con.cursor()
    result=cursor.execute("select* from Users where username= %s", [username])
    user=cursor.fetchone()
    return render_template('profile.html',user=user)


@app.route('/profile/<string:username>/edit',methods=['GET','POST'])
def edit_Profile(username):
    con=mysql.connect()
    cursor=con.cursor()
    data=cursor.execute("select* from Users where username= %s", [username])
    user2=cursor.fetchone()
    cursor.close()
    form=UserRegister(request.form)
    #change user infor
    form.first_name.data=user2[1]
    form.last_name.data=user2[2]
    form.email.data=user2[4]
    form.address.data=user2[5]
    form.username.data=user2[0]
    form.phone.data=user2[6]

    if request.method=='POST':
          first_name=request.form['first_name']
          last_name=request.form['last_name']
          email=request.form['email']
          address=request.form['address']
          username1=request.form['username']
          phone=request.form['phone']

          con=mysql.connect()
          cursor=con.cursor()
          query="update user set first_name=%s, last_name=%s, email=%s, address=%s, username=%s, phone=%s where username=%s"
          u=(first_name,last_name,email,address,username1,phone,username)
          cursor.execute("update Users set first_name=%s, last_name=%s, email=%s, address=%s, username=%s, phone=%s where username=%s",(first_name,last_name,email,address,username1,phone,username))
          con.commit()
          d2=cursor.fetchone()
          cursor.close()
          flash('User information updated!','success')
          return render_template('edit.html',form=form)
          #return redirect(url_for('edit'))

    return render_template('edit.html',form=form)




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
        #print(u['lat'], u['long'])
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
        #cursor.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('email'))
    return render_template('register.html', form=form)



'''Amy's section END'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

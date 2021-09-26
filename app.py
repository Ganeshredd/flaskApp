from os import name
from flask import Flask, render_template,session, url_for, request
from flask.templating import render_template_string
from flask_mysqldb import MySQL,MySQLdb
from werkzeug.utils import redirect
import yaml

app = Flask(__name__)
app.secret_key="123"

db =yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']


mysql =MySQL(app)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/club1")
def club1():
    return render_template('club1.html')


@app.route("/club2")
def club2():
    return render_template('club2.html')


@app.route("/club3")
def club3():
    return render_template('club3.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/formOutput", methods=['POST'])
def formOutput():
    if request.method =='POST':
        email = request.form.get("email")
        password = request.form.get("psw")
        ConfirmPassword = request.form.get("psw-repeat")
        Successfull = request.form.get("Successfull")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(email,password) VALUES(%s ,%s)",(  email,password))
        mysql.connection.commit()
        cur.close()
    return render_template('formOutput.html', email=email, password=password, ConfirmPassword=ConfirmPassword, Successfull=Successfull)

app.route("/new",methods=['GET','POST'])
def new_user():
    if request.method=="POST":
        if "one" in request.form and "two" in request.form:
            email=request.form['one']
            password=request.form['two']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO user(email,password) VALUES(%s ,%s)",(email,password))
            db.connection.commit()
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        if 'emailid' in request.form and 'password' in request.form:
            emailid= request.form['emailid']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (emailid, password,))
            account = cursor.fetchone()
            if account is not None:
                if account['email']==emailid and account['password']==password:
                    session['loginsuccess']=True
                    return redirect(url_for('loginlandingpage'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/new/loginlandingpage')
def loginlandingpage():
    if session['loginsuccess']==True:
        return render_template('loginlandingpage.html')

@app.route('/new/logout')
def logout():
    session.pop('loginsuccess',None)
    return redirect(url_for('home'))

@app.route('/user')
def user():
    cur = mysql.connection.cursor()
    resultValue =cur.execute("SELECT *FROM user;")
    mysql.connection.commit()
    if resultValue > 0:
        userDetails =cur.fetchall()
        print (userDetails)
    return render_template_string("user.html",userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)

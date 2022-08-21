from pickletools import read_uint1
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import mysql
import mysql.connector
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "cbee276e918a41aa63abe9d0ffb35d56f501606d47ec15ead6ca6e83f5e13769"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'hacka.py'
db = mysql.connector.connect(host='localhost', user='root', password = 'toor', database = 'hacka.py')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def reg():
    if 'loggedin' in session:
        return redirect("/dashboard")
    msg = ''
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        acc = cur.fetchone()
        if acc:
            msg = 'account exists'
        elif request.method == "POST" and "name" in request.form:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO users VALUES (NULL, %s, %s, %s, DEFAULT)", (name, email, password)) 
            mysql.connection.commit()
            cur.execute("INSERT INTO uinfo VALUES(NULL, %s, DEFAULT, DEFAULT, DEFAULT, DEFAULT)", [email])
            mysql.connection.commit()
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
            account = cur.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                session['name'] = account['name']
            msg = 'Registration Complete'
            return redirect("/dashboard")
        else:
            msg = 'Fill name'
    return render_template("reg.html", msg = msg)


@app.route("/login", methods=['GET', 'POST'])
def login():
    errmsg = ''
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['name'] = account['name']
            return redirect("/dashboard")
    else:
        errmsg= 'Invalid Data'
    if 'loggedin' in session:
        return redirect("/dashboard")
    return render_template("login.html", errmsg = errmsg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s", [session['id']])
        udata = cursor.fetchone()
        print(udata)
        if udata['role'] == 'admin':
            return redirect("/superuser")
        if request.method == "POST" and "usr-name" in request.form or "usr-password" in request.form or "usr-email" in request.form:
            email = request.form.get("usr-email")
            password = request.form.get("usr-password")
            name = request.form.get("usr-name")
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s", (name, email, password, session['id']))
            mysql.connection.commit()
            return redirect('/dashboard')
        return render_template("dashboard.html", udata = udata)
    return redirect("/login")

@app.route("/superuser")
def super():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s", [session['id']])
        udata = cur.fetchone()
        if udata['role'] == 'admin':
            return render_template("admin.html", udata = udata)
        return redirect('/dashboard')
    return redirect("/login")

@app.route('/virtuoso')
def vir():
    return render_template("virtuoso.html")

@app.route('/unlucky')
def unlucky():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if __name__ == "__main__":
    app.run(debug=True)
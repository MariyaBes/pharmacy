from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import re
import MySQLdb.cursors
from passlib.hash import sha256_crypt

from models import execute_read_query, execute_query

pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

app = Flask(__name__)

app.secret_key = 'no life'

mysql = MySQL(app)


def create_connection(host, user, password, db):
    connection = False
    try:
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = db
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        print("Connection to MySQL DB successful")
        connection = True
        return connection

    except MySQLdb.OperationalError as e:
        print(f'MySQL server has gone away: {e}, trying to reconnect')
        raise e


connect_db = create_connection('localhost', 'root', '6x7DeBYg83', 'mydb')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    email = request.form['email']
    password = request.form['password']
     
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'''SELECT * FROM user WHERE name = {email} AND password = {password}''')
    login_user = cursor.fetchone()
    print(login_user)
    # if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
    #     if sha256_crypt.verify(password, login_user['password']):
            
    #         if account:
    #             session['loggedin'] = True
    #             session['id'] = account['id']
    #             session['name'] = account['name']
    #             msg = 'Logged in successfully !'
    #             return render_template('index.html', msg = msg)
    #         else:
    #             msg = 'Incorrect username / password !'
    #         msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form.get('password2')
        password_hash= sha256_crypt.encrypt(request.form['password'])


        check_sql = f'''select * from user where email = "{email}"'''
        account = execute_read_query(connect_db, check_sql)

        if len(name) < 3:
            flash('Имя не должно быть короче 3 символов.', category='error')
        elif password != password2:
            flash('Пароли не совпадают', category='error')
        elif len(email) < 7:
            flash("Email должен быть длинее 7 символов.", category='error')
        elif re.match(pattern, email) is None:
            flash('Email неверный.', category='error')
        elif len(password) < 7:
            flash('Пароль должен быть не более 8 символов.', category='error')
        elif name[0].islower():
            flash('Имя и фамилия должны начинаться с заглавных букв.')
        else:
            password
            flash('Аккаунт создан!', category='success')
            write_sql = f'''INSERT INTO `user` ( `name`, `email`, `password`) 
            VALUES ('{name}', '{email}', '{password_hash}')'''
            execute_query(connect_db, write_sql)
            return redirect(url_for('login'))
    return render_template('signup.html', msg=msg)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
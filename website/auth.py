from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, flash
from flask_mysqldb import MySQL, MySQLdb
import re
from models import execute_read_query, execute_query

app = Flask(__name__)
mysql = MySQL(app)
pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

auth = Blueprint('auth', __name__)

def create_connection(localhost, root, password, mydb):
    connection = False
    try:
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'password'
        app.config['MYSQL_DB'] = 'mydb'
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        print("Connection to MySQL DB successful")
        connection = True
        return connection

    except MySQLdb.OperationalError as e:
        print(f'MySQL server has gone away: {e}, trying to reconnect')
        raise e


connection = create_connection('localhost', 'root', '6x7DeBYg83', 'mydb')



@auth.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    flash = ''
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        password2 = request.form.get('password2')
        
        check_sql = f'''select * from user where email = "{email}"'''
        account = execute_read_query(connection, check_sql)

        if account:
            flash('Аккаунт создан!', category='success')
        elif len(name) < 3:
            flash('Имя не должно быть короче 3 символов.', category='error')
        elif len(email) < 7:
            flash("Email должен быть длинее 7 символов.", category='error')
        elif re.match(pattern, email) is None:
            flash('Email неверный.', category='error')
        elif password != password2:
            flash('Пароли не совпадают', category='error')
        elif len(password) < 7:
            flash('Пароль должен быть не более 8 символов.', category='error')
        else:
            write_sql = f'''INSERT INTO 'user' ('email', 'password', 'name') 
            VALUES ('{email}', '{password}', '{name}')'''
            execute_query(connection, write_sql)
            return redirect(url_for('login'))

    return render_template('./templates/signup.html')
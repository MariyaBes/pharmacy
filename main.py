import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_mysqldb import MySQL, MySQLdb
from flask_login import LoginManager
import re
import datetime
import MySQLdb.cursors
from passlib.hash import sha256_crypt
from models import execute_read_query, execute_query
import base64
from PIL import Image


pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

app = Flask(__name__)

app.secret_key = 'YV_JNFVJW&*+96+_ETRBO_HOIQ+!FS'
app.permanent_session_lifetime = datetime.timedelta(seconds=300)

# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
# global COOKIE_TIME_OUT
# COOKIE_TIME_OUT = 60*5

login_manager = LoginManager()

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


connect_db = create_connection('localhost', 'root', '6x7DeBYg83', 'pharmacy')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute(f'''SELECT * FROM user WHERE email = "{email}"''')
        login_user = cursor.fetchone()
        print(login_user)
        try:
            if sha256_crypt.verify(password, login_user['password']):
                if login_user:
                    session['logged_in'] = True
                    session['id'] = login_user['id']
                    session['email'] = login_user['email']
                    return redirect(url_for('home'))
                # else:
                #     flash('Неправильный email/пароль пользователя!', category='error')
            else:
                flash('Неправильный email/пароль пользователя!', category='error')
        except TypeError as e:
            print(e)
            flash('Пользователь не найдет!', category='error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form.get('password2')
        password_hash = sha256_crypt.encrypt(request.form['password'])

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
            flash('Аккаунт создан!', category='success')
            write_sql = f'''INSERT INTO `user` ( `name`, `email`, `password`) 
            VALUES ('{name}', '{email}', '{password_hash}')'''
            execute_query(connect_db, write_sql)
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    cursor = mysql.connection.cursor()
    request_sql = f'''SELECT ID_Medication, Name, Date_of_storage, Price, Status, Billet, Del_Price, image_1, image_2
    from image, medication
    where medication.ID_Medication = image.id_image
    and ID_Medication = Image_id_image'''
    card_drug = execute_read_query(connect_db, request_sql)

    # binary = base64.b64decode(images).decode('ascii')
    # # img = Image.open(io.BytesIO(binary))
    # print(binary)
    # # img.show()
    # file = request.files['file']
    # extension = os.path.splitext(file.filename)[1]
    # f_name = str(uuid.uuid4()) + extension
    return render_template('index.html', log_in = session.get('logged_in'), card_drug = card_drug)


@app.route('/cart/<int:ID_Medication>', methods=['GET', 'POST'])
def cart(ID_Medication):
    cart_sql = f'''SELECT ID_Medication, Name, Description, Price, Billet, image_1, image_2, image_3, Title, Address, Country, Category, Apllication, Release_Conditions, Contraindications, Side_Effects, Dose
    from medication, image, provider, marking
    where ID_Medication = "{ID_Medication}"
    and medication.ID_Medication = image.id_image
    and ID_Medication = Image_id_image
    and ID_Medication = marking.ID_Marking
    and medication.ID_Medication = provider.ID_Provider
    '''
    card_product = execute_read_query(connect_db, cart_sql)
    return render_template('card.html', card_product = card_product)

@app.route('/basket', methods=['GET', 'POST'])
def basket ():
    cursor = None
    if request.method == "POST":
        id = request.form['product_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT ID_Medication FROM medication WHERE ID_Medication=%s", id)
        row = cursor.fetchone()
        # id_sql = (f'''SELECT ID_Medication from medication where ID_Medication=%s''', id)
        # id_product = execute_read_query(connect_db, id_sql)
        print(row)
        print(id)
        backet_sql = f'''SELECT ID_Medication, Name, Price, image_1
        from medication, image
        where medication.ID_Medication = image.id_image
        and ID_Medication = Image_id_image
        and ID_Medication = {id}
        '''
        basket_product = execute_read_query(connect_db, backet_sql)

    return render_template('basket.html', basket=basket_product)




if __name__ == '__main__':
    app.run(debug=True)

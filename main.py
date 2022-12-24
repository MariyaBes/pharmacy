import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash, json
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
app.permanent_session_lifetime = datetime.timedelta(seconds=900)

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
    user_id = session.get('id');
    print(user_id)

    request_sql = f'''SELECT ID_Medication, Name, Date_of_storage, Price, Status, Billet, Del_Price, image_1, image_2
    from image, medication
    where medication.ID_Medication = image.id_image
    and ID_Medication = Image_id_image'''
    card_drug = execute_read_query(connect_db, request_sql)

    basket_sql = f'''SELECT ID_Medication, Cost, title, image, Count, ID_Order
    from order_cart
    where ID_User = "{user_id}"
    group by ID_Order'''
    basket = execute_read_query(connect_db, basket_sql)
    
    cart_count_sql = f'''SELECT count(ID_Order) as count_cart
    from order_cart
    where ID_Medication > 0
    and ID_User = "{user_id}"'''
    cart_count = execute_read_query(connect_db, cart_count_sql)

    total_cost_count_sql = f'''SELECT sum(Cost*Count) as total_cost_count
    from order_cart
    where ID_User = "{user_id}"'''
    total_cost_count = execute_read_query(connect_db, total_cost_count_sql)

    return render_template('index.html', log_in = session.get('logged_in'), card_drug = card_drug, basket = basket, cart_count = cart_count, total_cost_count = total_cost_count)


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

    user_id = session.get('id');
    print(user_id)

    basket_sql = f'''SELECT ID_Medication, Cost, title, image, Count, ID_Order
    from order_cart
    where ID_User = "{user_id}"
    group by ID_Order'''
    basket = execute_read_query(connect_db, basket_sql)
    
    cart_count_sql = f'''SELECT count(ID_Order) as count_cart
    from order_cart
    where ID_Medication > 0
    and ID_User = "{user_id}"'''
    cart_count = execute_read_query(connect_db, cart_count_sql)

    total_cost_count_sql = f'''SELECT sum(Cost*Count) as total_cost_count
    from order_cart
    where ID_User = "{user_id}"'''
    total_cost_count = execute_read_query(connect_db, total_cost_count_sql)
   

    return render_template('card.html', card_product = card_product, basket = basket, cart_count = cart_count, total_cost_count = total_cost_count)

@app.route('/basket', methods=['POST'])
def basket ():
    id_product = request.form['id'];
    title_product = request.form['title'];
    price = request.form['price'];
    image = request.form['img'];
    count = request.form['count'];

    print (json.dumps({'id': id_product,
    'title': title_product,
    'price': price,
    'image': image,
    'count': count}))

    cart_sql = f'''INSERT INTO `order_cart` (`Cost`, `title`, `ID_Medication`, `image`, `Count`, `ID_User`) VALUES ('{price}', '{title_product}', '{id_product}', '{image}', '{count}', '{session.get('id')}')'''
    return execute_query(connect_db, cart_sql)

@app.route('/del_item', methods=['POST'])
def del_item ():
    id_del = request.form['id_del']
    print (id_del)
    print (json.dumps({'id': id_del}))
    del_sql = f'''DELETE FROM `pharmacy`.`order_cart` WHERE (`ID_Order` = '{id_del}')'''
    return execute_query(connect_db, del_sql)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    name_id_user = session.get('id')

    basket_sql = f'''SELECT ID_Medication, Cost, title, image, Count, ID_Order
    from order_cart
    where ID_User = "{name_id_user}"
    group by ID_Order'''
    basket = execute_read_query(connect_db, basket_sql)

    order_pay = f'''SELECT ID_Order, sum(Cost*Count) as total_cost_count
    from order_cart
    where ID_User = "{name_id_user}"'''
    order = execute_read_query(connect_db, order_pay)

    get_user_sql = f'''SELECT name
    from user
    where id = "{name_id_user}"'''
    get_user = execute_read_query(connect_db, get_user_sql)

    adr_sql = f'''SELECT distinct Address
    from delivery
    where User_id = "{name_id_user}"'''
    adr = execute_read_query(connect_db, adr_sql)

    if request.form.get('clear_order'):
        
        del_order = f'''DELETE FROM `order_cart` WHERE `ID_Order` IN ('{request.form.get('clear_order')}')'''
        execute_query(connect_db, del_order)
        return redirect('/')

    return render_template('pay.html', order=order, get_user=get_user, adr=adr, basket=basket)

@app.route('/order-form', methods=['GET', 'POST'])
def order_modal():
    order_pay = f'''SELECT ID_Order, sum(Cost*Count) as total_cost_count
    from order_cart
    where ID_User = "{session.get('id')}"'''

    cart_count_sql = f'''SELECT count(ID_Order) as count_cart
    from order_cart
    where ID_Medication > 0
    and ID_User = "{session.get('id')}"'''
    cart_count = execute_read_query(connect_db, cart_count_sql)

    order = execute_read_query(connect_db, order_pay)

    if request.method == "POST":
        address = request.form.get('address')
        id_order = request.form.get('id_order')
        order_type = request.form.get('order-type')
        paymant = request.form.get('payment-method')

        write_sql = f'''INSERT INTO `delivery` (`Delivery`, `Order_ID_Order`, `Pl_cost`, `User_id`, `Address`, `Methods_payment`) 
        VALUES ('{order_type}', '{id_order}', '149', '{session.get('id')}', '{address}', '{paymant}')'''
        execute_query(connect_db, write_sql)
        return redirect('/pay')

    return render_template ('modal.html', order = order, count = cart_count)

if __name__ == '__main__':
    app.run(debug=True)

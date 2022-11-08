from flask import Blueprint, render_template, request, flash
import re

pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(name) < 3:
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
            flash('Аккаунт создан!', category='success')

    return render_template('signup.html')
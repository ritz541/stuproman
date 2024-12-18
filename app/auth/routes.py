from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import mongo

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data})
        if user and check_password_hash(user['password_hash'], form.password.data):
            user_obj = User(user)
            login_user(user_obj, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Invalid email or password')
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if mongo.db.users.find_one({'email': form.email.data}):
            flash('Email already registered')
            return redirect(url_for('auth.register'))
        
        user_data = {
            'email': form.email.data,
            'username': form.username.data,
            'password_hash': generate_password_hash(form.password.data)
        }
        mongo.db.users.insert_one(user_data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

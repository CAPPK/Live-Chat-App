from flask import Blueprint, Flask, redirect, request, render_template, url_for, flash
from google.cloud import datastore
from werkzeug.security import generate_password_hash, check_password_hash
# datastore_client = datastore.Client()
# #import random
from datetime import datetime
# from .main import datastore_client

from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth', __name__)


# @auth.route('/')
# def root():
#     return render_template("/home/home.html", code=302)


# @auth.route('/home', methods=['GET'])
# def home():
#     return render_template("/home/home.html", code=302)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    usernameInput = ''
    passwordInput = ''
    if request.method == 'POST':
        usernameInput = request.form['Username']
        passwordInput = request.form['Password']
        from models import User, loading_user
        user = loading_user(usernameInput, passwordInput)
        if user:
            login_user(user, remember=True)
            return redirect(url_for('homeProfile'))
        else:
            flash('Please check login details and try again')
            return redirect(url_for('auth.login'))
    return render_template("/login/login.html", code=302)


@auth.route('/createuser', methods=['GET', 'POST'])
def createuser():
    from main import datastore_client
    usernameInput = ''
    passwordInput = ''
    if request.method == 'POST':
        usernameInput = request.form['Username']
        passwordInput = request.form['Password']

        query = datastore_client.query(kind='User')
        query.add_filter('username', '=', usernameInput)
        match = list(query.fetch())
        if match:
            flash('Username is already in use')
            return redirect(url_for('auth.createuser'))
        else:
            kind = 'User'
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            name = 'User '+date_time
            # # The Cloud Datastore key for the new entity
            task_key = datastore_client.key(kind, name)
            # # Prepares the new entity
            task = datastore.Entity(key=task_key)
            task['username'] = usernameInput
            task['password'] = generate_password_hash(
                passwordInput, method='sha256')
            datastore_client.put(task)

            kind = 'Conversations'
            name = usernameInput
            task_key = datastore_client.key(kind, name)
            task = datastore.Entity(key=task_key)
            task['activeConvos'] = []
            datastore_client.put(task)

            # kind='PrivateMessage'
            # task_key = datastore_client.key(kind, name)
            # task = datastore.Entity(key=task_key)
            # task['activeConvos'] = []
            # datastore_client.put(task)


            return redirect(url_for('auth.login'))
    return render_template("/createuser/createuser.html", code=302)


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)

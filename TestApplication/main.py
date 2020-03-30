
from auth import auth as auth_blueprint
from flask import Blueprint, Flask, redirect, request, render_template, url_for
from google.cloud import datastore
from datetime import datetime
from flask_login import login_required, current_user, LoginManager

datastore_client = datastore.Client()
main = Blueprint('main', __name__)


def create_app():
    """Construct the core app object."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super secret key'

    app.register_blueprint(auth_blueprint)

    app.register_blueprint(main)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from models import User, getUser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return getUser(user_id)

    return app


app = create_app()


@app.route('/')
def root():
    return render_template("/home/home.html", code=302)


@app.route('/home', methods=['GET'])
def home():
    return render_template("/home/home.html", code=302)


@app.route('/homeProfile', methods=['GET'])
@login_required
def homeProfile():
    return render_template("/homeProfile/homeProfile.html", ActiveUser=current_user.id, code=302)


@app.route('/livechat', methods=['GET', 'POST'])
def livechat():
    newMessage = ''
    if request.method == 'POST':
        newMessage = request.form['Msg']
    if newMessage:
        kind = 'Messages'
        # name = 'Message'
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        name = 'Message '+date_time
        # # The Cloud Datastore key for the new entity
        task_key = datastore_client.key(kind, name)
        # # Prepares the new entity
        task = datastore.Entity(key=task_key)
        task['message'] = newMessage
        task['time'] = now
        # # Saves the entity
        datastore_client.put(task)

        query = datastore_client.query(kind='Messages')
        query.order = ['-time']
        msgs = query.fetch(10)
        # print(query.fetch(1))
        # print(datastore_client.get(task_key))
        return render_template('livechat/livechat.html', msgs=msgs)
    query = datastore_client.query(kind='Messages')
    query.order = ['-time']
    msgs = query.fetch(10)
    return render_template('livechat/livechat.html', msgs=msgs)
    # return render_template('livechat/livechat.html')


@app.route('/privateSearchUser', methods=['GET', 'POST'])
@login_required
def privateSearchUser():
    toID = ''
    fromID = ''
    toMessage = ''

    if request.method == 'POST':
        fromID = current_user.id
        toID = request.form['toID']
        toMessage = request.form['Msg']
    if toMessage:
        kind = 'PrivateMessage'
        # name = 'Message'
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        name = 'Message '+date_time
        # # The Cloud Datastore key for the new entity
        task_key = datastore_client.key(kind, name)
        # # Prepares the new entity
        task = datastore.Entity(key=task_key)
        task['message'] = toMessage
        task['time'] = now
        task['toID'] = toID
        task['fromID'] = fromID
        # # Saves the entity
        datastore_client.put(task)

        query = datastore_client.query(kind='PrivateMessage')
        query.add_filter('toID', '=', current_user.id)
        #query.order = ['-time']
        msgs = query.fetch()
        return render_template('privateSearchUser/privateSearchUser.html', msgs=msgs, ActiveUser=current_user.id)
    query = datastore_client.query(kind='PrivateMessage')
    query.add_filter('toID', '=', current_user.id)
    # query.order = ['-time']
    msgs = query.fetch()
    return render_template('privateSearchUser/privateSearchUser.html', msgs=msgs, ActiveUser=current_user.id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

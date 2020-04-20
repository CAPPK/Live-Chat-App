
from auth import auth as auth_blueprint
from flask import Blueprint, Flask, redirect, request, render_template, url_for,flash
from google.cloud import datastore
from datetime import datetime
from flask_login import login_required, current_user, LoginManager
from itertools import chain

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
        if current_user.is_authenticated:
            
            if request.form.get('anon'):
                task['message'] = newMessage
            else:
                task['message'] =current_user.id+": " +newMessage
        else:
            task['message'] = newMessage
        task['time'] = now
        task['timeToShow']=now.strftime("%x %X")
        # # Saves the entity
        datastore_client.put(task)

        query = datastore_client.query(kind='Messages')
        query.order = ['-time']
        msgs = query.fetch(10)
        return render_template('livechat/livechat.html', msgs=msgs)
    query = datastore_client.query(kind='Messages')
    query.order = ['-time']
    msgs = query.fetch(10)
    return render_template('livechat/livechat.html', msgs=msgs)


@app.route('/privateconvo', methods=['GET', 'POST'])  # in progress
@login_required
def privateconvo():
    if request.method == 'POST':  # user input a new conversation
        from models import checkIfUser
        toID = request.form['NewConvo']
        if checkIfUser(toID):  # if user was valid, update both current and end user conversations
            kind = 'Conversations'
            name = current_user.id
            task_key = datastore_client.key(kind, name)
            task = datastore_client.get(task_key)
            if toID not in task['activeConvos'] and toID != current_user.id:
                task['activeConvos'].append(toID)
                # updates the current users active convos
                datastore_client.put(task)
                name = toID
                task_key = datastore_client.key(kind, name)
                task = datastore_client.get(task_key)
                task['activeConvos'].append(current_user.id)
                datastore_client.put(task)

                kind="PrivateMessage"#setting up the array to hold the conversation
                name=current_user.id+toID
                task_key=datastore_client.key(kind,name)
                task=datastore.Entity(key=task_key)
                task['activeConvos'] = []
                datastore_client.put(task)

                kind="PrivateMessage"#setting up the array to hold the conversation
                name=toID+current_user.id
                task_key=datastore_client.key(kind,name)
                task=datastore.Entity(key=task_key)
                task['activeConvos'] = []
                datastore_client.put(task)
            else:
                flash('You already have a conversation with them silly goose')
        else:
            flash('This user does not exist')
    task_key = datastore_client.key('Conversations', current_user.id)
    task = datastore_client.get(task_key)
    conversations=task['activeConvos']
    return render_template('privateconvo/privateconvo.html', conversations=conversations, ActiveUser=current_user.id)

@app.route('/privateSearchUser', defaults={'usersID': 'temporary'})
@app.route('/privateSearchUser/<usersID>', methods=['GET', 'POST'])
@login_required
def privateSearchUser(usersID):
    toMessage = ''
    # print(usersID+"'s messages")
    if request.method == 'POST':
        toMessage = request.form['Msg']
    if toMessage:
        task_key = datastore_client.key('PrivateMessage', current_user.id+usersID)
        task = datastore_client.get(task_key)
        task['activeConvos'].append(current_user.id +": " + toMessage)
        conversation=task['activeConvos']
        datastore_client.put(task)

        task_key = datastore_client.key('PrivateMessage', usersID+current_user.id)
        task = datastore_client.get(task_key)
        task['activeConvos'].append(current_user.id +": " + toMessage)
        conversation=task['activeConvos']
        datastore_client.put(task)
        
        return render_template('privateSearchUser/privateSearchUser.html', msgs=conversation, ActiveUser=current_user.id,userID=usersID)
    
    task_key = datastore_client.key('PrivateMessage', current_user.id+usersID)
    task = datastore_client.get(task_key)
    conversations=task['activeConvos']
    return render_template('privateSearchUser/privateSearchUser.html', msgs=conversations, ActiveUser=current_user.id,userID=usersID )



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

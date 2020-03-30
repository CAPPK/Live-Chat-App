
from auth import auth as auth_blueprint
from flask import Blueprint, Flask, redirect, request, render_template
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
    

@app.route('/privateConvo', methods=['GET', 'POST'])
def privateConvo():
    newMessage = ''
    if request.method == 'POST':
        newMessage = request.form['Msg']
    if newMessage:
        fromCurrentUsername = current_user.id
        toOtherUsername = request.form['toUser']
        kind='Private Message'
        # name = 'Message'
        now=datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        name='Private Message '+date_time
        # # The Cloud Datastore key for the new entity
        task_key = datastore_client.key(kind, name)
        # # Prepares the new entity
        task = datastore.Entity(key=task_key)
        task['message'] = newMessage
        task['time']=now
        # # Saves the entity
        datastore_client.put(task)

    query1=datastore_client.query(kind='Private Message')
    # May need to be ''+time', check afterwards
    query1.order=['-time']
    allMessages = query1.fetch()
    relevantMessages = []

    # Get all messages with the entered usernamed as fromUsername and toUsername
    for entity in allMessages:
        if entity[fromUsername] == fromCurrentUsername or entity[fromUsername] == toOtherUsername:
            if entity[toUsername] == fromCurrentUsername or entity[toUsername] == toOtherUsername:
                relevantMessages.append(entity)

    return render_template('privatemessage/privateConvo.html', msgs=relevantMessages, toUsername=toOtherUsername)
    #return render_template('livechat/livechat.html')

@app.route('/privatemessage', methods=['GET', 'POST'])
def privatemessage():
    # fromUsernameInput = ''
    toUsernameInput = ''

    if request.method == 'POST':
        fromUsernameInput = current_user.id
        toUsernameInput = request.form['toUsernameIn']

        # Verify fromUsername is valid
        # fromQuery = datastore_client.query(kind='User')
        # fromQuery.add_filter('username', '=', fromUsernameInput)
        # fromUserMatch = list(fromQuery.fetch())
        #
        # if fromUserMatch:
        #     # Verify toUsername is valid
        #     toQuery = datastore_client.query(kind='User')
        #     toQuery.add_filter('username', '=', toUsernameInput)
        #     toUserMatch = list(query.fetch())
        if toUserMatch:
            # Get all private messages from datastore
            query1=datastore_client.query(kind='Private Message')
            # May need to be ''+time', check afterwards
            query1.order=['-time']
            allMessages = query1.fetch()
            relevantMessages = []

            # Get all messages with the entered usernamed as fromUsername and toUsername
            for entity in allMessages:
                if entity[fromUsername] == fromUsernameInput or entity[fromUsername] == toUsernameInput:
                    if entity[toUsername] == fromUsernameInput or entity[toUsername] == toUsernameInput:
                        relevantMessages.append(entity)

                # query1=datastore_client.query(kind='Private Message')
                # query1.add_filter('fromUsername', '=', fromUsernameInput)
                # query1.add_filter('toUsername', '=', toUsernameInput)
                # msgs1=query.fetch(10)
                #
                # query2=datastore_client.query(kind='Private Message')
                # query2.add_filter('fromUsername', '=', toUsernameInput)
                # query2.add_filter('toUsername', '=', fromUsernameInput)
                # msgs2=query.fetch(10)

                # msgs = msgs1 + msgs2
                # msgs.sort(key=lambda x: x.count, reverse=True)

                return render_template('privatemessage/privateConvo.html', msgs=relevantMessages, toUsername=toUsernameInput)

        # if the request was not POST or the usernames they entered for Private Messaging were invalid, refresh the page
    return render_template("/privatemessage/privateSearchUser.html", code=302)





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

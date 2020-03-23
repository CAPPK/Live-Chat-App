from flask import Flask, redirect, request, render_template
from google.cloud import datastore
datastore_client = datastore.Client()
#import random
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def root():
    return render_template("/home/home.html", code=302)


@app.route('/home', methods=['GET'])
def home():
    return render_template("/home/home.html", code=302)


@app.route('/homeProfile', methods=['GET'])
def homeProfile():
    return render_template("/homeProfile/homeProfile.html", code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    usernameInput = ''
    passwordInput = ''
    if request.method == 'POST':
        usernameInput = request.form['Username']
        passwordInput = request.form['Password']

        query = datastore_client.query(kind='User')
        query.add_filter('username', '=', usernameInput)
        query.add_filter('password', '=', passwordInput)
        # query.projection = ['priority']
        match = list(query.fetch())
        if match:
            query2 = datastore_client.query(kind='Session')
            query2.add_filter('username', '=', usernameInput)
            # query.projection = ['priority']
            match2 = list(query2.fetch())
            if match2:
                return render_template("/homeProfile/homeProfile.html", ActiveUser=usernameInput)
            else:
                kind = 'Session'
                name = usernameInput
                # # The Cloud Datastore key for the new entity
                task_key = datastore_client.key(kind, name)
                # # Prepares the new entity
                task = datastore.Entity(key=task_key)
                task['username'] = usernameInput
                task['session'] = 'Yes'
                datastore_client.put(task)
                return render_template("/homeProfile/homeProfile.html", ActiveUser=usernameInput)
        else:
            return render_template("/createuser/createuser.html", code=302)
    return render_template("/login/login.html", code=302)


@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
    usernameInput = ''
    passwordInput = ''
    if request.method == 'POST':
        usernameInput = request.form['Username']
        passwordInput = request.form['Password']

        query = datastore_client.query(kind='User')
        query.add_filter('username', '=', usernameInput)
        match = list(query.fetch())
        if match:
            return render_template("/createuser/createuser.html", code=302)
        else:
            kind = 'User'
            now=datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            name='User '+date_time
            # # The Cloud Datastore key for the new entity
            task_key = datastore_client.key(kind, name)
            # # Prepares the new entity
            task = datastore.Entity(key=task_key)
            task['username'] = usernameInput
            task['password'] = passwordInput
            datastore_client.put(task)
            return render_template("/home/home.html", code=302)
    return render_template("/createuser/createuser.html", code=302)


@app.route('/livechat', methods=['GET', 'POST'])
def livechat():
    newMessage = ''
    if request.method == 'POST':
        newMessage = request.form['Msg']
    if newMessage:
        kind='Messages'
        # name = 'Message'
        now=datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        name='Message '+date_time
        # # The Cloud Datastore key for the new entity
        task_key = datastore_client.key(kind, name)
        # # Prepares the new entity
        task = datastore.Entity(key=task_key)
        task['message'] = newMessage
        task['time']=now
        # # Saves the entity
        datastore_client.put(task)

        query=datastore_client.query(kind='Messages')
        query.order=['-time']
        msgs=query.fetch(10)
        #print(query.fetch(1))
        #print(datastore_client.get(task_key))
        return render_template('livechat/livechat.html', msgs=msgs)
    query=datastore_client.query(kind='Messages')
    query.order=['-time']
    msgs=query.fetch(10)
    return render_template('livechat/livechat.html', msgs=msgs)
    #return render_template('livechat/livechat.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

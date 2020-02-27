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

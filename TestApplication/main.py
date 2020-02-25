from flask import Flask, redirect, request


app = Flask(__name__)


@app.route('/')
def root():
    return redirect("/static/home.html", code=302)


@app.route('/livechat', methods=['GET', 'POST'])
def livechat():
    newMessage = ''
    if request.method == 'POST':
        newMessage = request.form['Msg']
    if newMessage:
        print(newMessage)
        # from google.cloud import datastore
        # # Instantiate a client
        # datastore_client = datastore.Client()
        # kind = 'Messages'
        # name = 'Message'
        # # The Cloud Datastore key for the new entity
        # task_key = datastore_client.key(kind, name)
        # # Prepares the new entity
        # task = datastore.Entity(key=task_key)
        # task['message'] = newMessage
        # # Saves the entity
        # datastore_client.put(task)

    return redirect("/static/livechat.html", code=302)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

# from .main import datastore
# from .main import datastore_client
from auth import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    """A user for the application."""

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def to_dict(self):
        return {
            'username': self.id,
            'password': self.password,
        }


def loading_user(usernameInput, userpassword):
    from main import datastore
    from main import datastore_client
    query = datastore_client.query(kind='User')
    query.add_filter('username', '=', usernameInput)
    match = list(query.fetch())
    password = ''
    # print(match)
    for task in query.fetch():
        password = task['password']
    if match and check_password_hash(password, userpassword):
        return User(usernameInput, password)
    return None


def getUser(usernameInput):
    from main import datastore
    from main import datastore_client
    query = datastore_client.query(kind='User')
    query.add_filter('username', '=', usernameInput)
    match = list(query.fetch())
    password = ''
    for task in query.fetch():
        password = task['password']
    if match:
        return User(usernameInput, password)
    return None

from flask_login import UserMixin
from app import login_manager, mongo
from bson import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.id = str(user_data.get('_id'))
        self.email = user_data.get('email')
        self.username = user_data.get('username')

    @staticmethod
    def check_email(email):
        return mongo.db.users.find_one({'email': email})

@login_manager.user_loader
def load_user(id):
    try:
        u = mongo.db.users.find_one({'_id': ObjectId(id)})
        if not u:
            return None
        return User(u)
    except:
        return None

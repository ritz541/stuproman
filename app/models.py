from flask_login import UserMixin
from app import login_manager, mongo
from bson import ObjectId
from datetime import datetime

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

class Project:
    def __init__(self, project_data):
        self.id = str(project_data.get('_id'))
        self.name = project_data.get('name')
        self.description = project_data.get('description')
        self.goals = project_data.get('goals', [])
        self.requirements = project_data.get('requirements', [])
        self.created_by = project_data.get('created_by')
        self.created_at = project_data.get('created_at')
        self.updated_at = project_data.get('updated_at')
        self.status = project_data.get('status', 'active')
        self.collaborators = project_data.get('collaborators', [])

    @staticmethod
    def create_project(name, description, goals, requirements, user_id):
        project = {
            'name': name,
            'description': description,
            'goals': goals,
            'requirements': requirements,
            'created_by': user_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'active',
            'collaborators': [user_id]
        }
        result = mongo.db.projects.insert_one(project)
        return str(result.inserted_id)

    @staticmethod
    def get_project(project_id):
        try:
            project = mongo.db.projects.find_one({'_id': ObjectId(project_id)})
            return Project(project) if project else None
        except:
            return None

    @staticmethod
    def get_user_projects(user_id):
        projects = mongo.db.projects.find({
            '$or': [
                {'created_by': user_id},
                {'collaborators': user_id}
            ]
        }).sort('updated_at', -1)
        return [Project(project) for project in projects]

    def update(self, data):
        data['updated_at'] = datetime.utcnow()
        mongo.db.projects.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': data}
        )

    def delete(self):
        mongo.db.projects.delete_one({'_id': ObjectId(self.id)})

from flask import render_template
from flask_login import login_required, current_user
from app.main import bp
from app.models import Project

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Get the user's recent projects
    recent_projects = Project.get_user_projects(current_user.id)[:3]
    return render_template('index.html', title='Dashboard', 
                         recent_projects=recent_projects)

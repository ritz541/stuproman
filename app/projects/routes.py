from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.projects import bp
from app.projects.forms import ProjectForm
from app.models import Project
from bson import ObjectId

@bp.route('/projects')
@login_required
def list_projects():
    projects = Project.get_user_projects(current_user.id)
    return render_template('projects/list.html', title='My Projects', projects=projects)

@bp.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        goals = [goal.strip() for goal in form.goals.data.split('\n') if goal.strip()]
        requirements = [req.strip() for req in form.requirements.data.split('\n') if req.strip()]
        
        project_id = Project.create_project(
            name=form.name.data,
            description=form.description.data,
            goals=goals,
            requirements=requirements,
            user_id=current_user.id
        )
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.view_project', project_id=project_id))
    return render_template('projects/create.html', title='Create Project', form=form)

@bp.route('/projects/<project_id>')
@login_required
def view_project(project_id):
    project = Project.get_project(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('projects.list_projects'))
    if current_user.id not in project.collaborators:
        flash('You do not have access to this project.', 'error')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/view.html', title=project.name, project=project)

@bp.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.get_project(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('projects.list_projects'))
    if project.created_by != current_user.id:
        flash('You do not have permission to edit this project.', 'error')
        return redirect(url_for('projects.list_projects'))
    
    form = ProjectForm()
    if form.validate_on_submit():
        goals = [goal.strip() for goal in form.goals.data.split('\n') if goal.strip()]
        requirements = [req.strip() for req in form.requirements.data.split('\n') if req.strip()]
        
        project.update({
            'name': form.name.data,
            'description': form.description.data,
            'goals': goals,
            'requirements': requirements,
            'status': form.status.data
        })
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    elif request.method == 'GET':
        form.name.data = project.name
        form.description.data = project.description
        form.goals.data = '\n'.join(project.goals)
        form.requirements.data = '\n'.join(project.requirements)
        form.status.data = project.status
    
    return render_template('projects/edit.html', title='Edit Project', form=form, project=project)

@bp.route('/projects/<project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.get_project(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('projects.list_projects'))
    if project.created_by != current_user.id:
        flash('You do not have permission to delete this project.', 'error')
        return redirect(url_for('projects.list_projects'))
    
    project.delete()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects.list_projects'))

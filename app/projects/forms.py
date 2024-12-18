from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    goals = TextAreaField('Goals', validators=[DataRequired(), Length(min=10, max=1000)])
    requirements = TextAreaField('Requirements', validators=[DataRequired(), Length(min=10, max=1000)])
    status = SelectField('Status', choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled')
    ])
    submit = SubmitField('Create Project')

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Department Email')
    submit = SubmitField('Submit')

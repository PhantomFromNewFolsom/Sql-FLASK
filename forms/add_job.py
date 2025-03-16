from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = StringField('Team leader id', validators=[DataRequired()])
    job = StringField("Job Title", validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    is_finished = BooleanField('Is finished?')
    submit = SubmitField('Submit')

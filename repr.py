from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, EmailField
from wtforms.validators import DataRequired

from data.db_session import global_init, create_session
from data.jobs import Job
from main import add_user


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    second_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

global_init(f'db/blogs.db')


@app.route('/table')
def table():
    db_sess = create_session()
    lst = []
    for job in db_sess.query(Job).all():
        lst.append(job)
    return render_template('table.html', title='Работа', list=lst)


@app.route('/success')
def success():
    return '''<h1>Успех!</h1>'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        add_user(request.form['name'], request.form['surname'], int(request.form['age']), request.form['position'],
                 request.form['speciality'], request.form['address'], request.form['email'])
        return redirect('/success')
    return render_template('form.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

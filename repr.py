from flask import Flask, render_template, redirect
from data import db_session
from data.db_session import global_init, create_session
from data.jobs import Job
from data.users import User

from flask_login import LoginManager, login_user, logout_user, login_required

from forms.add_job import JobForm
from forms.login import LoginForm
from forms.reg import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

global_init(f'db/blogs.db')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.second_password.data:
            return render_template('form.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('form.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('form.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Job(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)


@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    form = JobForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == job_id).first()

        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data

        db_sess.commit()
        return redirect('/')

    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == int(job_id)).first()

    form.team_leader.data = job.team_leader
    form.job.data = job.job
    form.work_size.data = job.work_size
    form.collaborators.data = job.collaborators
    form.start_date.data = job.start_date
    form.end_date.data = job.end_date
    form.is_finished.data = job.is_finished

    return render_template('add_job.html', form=form)


@app.route('/confirm/<job_id>')
def confirm(job_id):
    return render_template('confirmation.html', id=job_id)


@app.route('/delete_job/<job_id>')
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        return redirect('/')
    else:
        return 404


@app.route('/index')
@app.route('/')
def index():
    db_sess = create_session()
    lst = []
    for job in db_sess.query(Job).all():
        lst.append(job)
    return render_template('home.html', title='Милый дом', list=lst)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

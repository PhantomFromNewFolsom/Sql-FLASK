from flask import Flask, render_template, redirect
from flask_restful import Api

from data.db_session import global_init, create_session
from data.departments import Department
from data.jobs import Job
from data.users import User

from flask_login import LoginManager, login_user, logout_user, login_required

from forms.add_job import JobForm
from forms.department import DepartmentForm
from forms.login import LoginForm
from forms.reg import RegisterForm

from data import db_session, users_api, restful_api, restful_job_api
from yandex_maps import search, get_image
from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)

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
    return render_template('add_job.html', title='Добавление работы', form=form)


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

    return render_template('add_job.html', title='Редактирование работы', form=form)


@app.route('/confirm/<job_id>')
def confirm(job_id):
    return render_template('confirmation.html', title='Уверен?', id=job_id)


@app.route('/confirm_dep/<department_id>')
def confirm_dep(department_id):
    return render_template('confirmation_dep.html', title='Уверен?', id=department_id)


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


@app.route('/department_list')
def department_list():
    db_sess = create_session()
    lst = []
    for department in db_sess.query(Department).all():
        lst.append(department)
    return render_template('department_list.html', title='Список департаментов', list=lst)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Department).filter(Department.email == form.email.data).first():
            return render_template('edit_department.html',
                                   title='Редактирование департамента', form=form,
                                   message="Департамент с таким email уже есть")
        department = Department()

        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data

        db_sess.add(department)
        db_sess.commit()
        return redirect('/department_list')

    return render_template('edit_department.html', title='Добавление департамента', form=form)


@app.route('/edit_department/<department_id>', methods=['GET', 'POST'])
def edit_department(department_id):
    form = DepartmentForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id).first()

        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data

        db_sess.commit()
        return redirect('/department_list')

    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()

    form.title.data = department.title
    form.chief.data = department.chief
    form.members.data = department.members
    form.email.data = department.email

    return render_template('edit_department.html', title='Редактирование департамента', form=form)


@app.route('/delete_department/<department_id>')
def delete_department(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
        return redirect('/department_list')
    else:
        return 404


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    db_sess = db_session.create_session()
    user = get(f'http://localhost:8081/api/v2/users/{user_id}').json()['user']
    if user:
        get_image(*search(user["city_from"]))
        return render_template('users_show.html',
                               title=f'{user["surname"]} {user["name"]}: {user["city_from"]}', img='../static/images/map.png',
                               user=f'{user["name"]} {user["surname"]}', city_from=user["city_from"])
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


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(users_api.blueprint)

    # для списка объектов
    api.add_resource(restful_api.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(restful_api.UsersResource, '/api/v2/users/<user_id>')

    # для списка объектов
    api.add_resource(restful_job_api.JobsListResource, '/api/v2/jobs')

    # для одного объекта
    api.add_resource(restful_job_api.JobsResource, '/api/v2/jobs/<job_id>')
    app.run(port=8081, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()

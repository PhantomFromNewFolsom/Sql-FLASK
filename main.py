from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Job
from data.departments import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_user(name, surname, age, position, speciality, address, email, password):
    user = User()
    user.name = name
    user.surname = surname
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    user.set_password(password)
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)

    add_user("Scot", "Ridley", 21, "captain", "research engineer",
             "module_1", "scott_chief@mars.org", '1')

    add_user("Alex", "Pushkin", 19, "boatswain", "ecobiolog",
             "module_1", "PushKing@mars.org", '2')

    add_user("Pro", "Gamer", 14, "boatswain", "ecobiolog",
             "module_2", "Gosswrtiter@mars.org", '3')

    add_user("Adam", "Smitt", 29, "chef", "cook",
             "module_1", "galaktika@mars.org", '4')

    add_user("Yop", "Yan", 21, "cabin boy", "doctor",
             "module_1", "ThisIsHorosho@mars.org", '5')

    job = Job()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.is_finished = False
    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()

    job = Job()
    job.team_leader = 2
    job.job = "distraction of meteorites and comets"
    job.work_size = 26
    job.collaborators = "1, 2, 3"
    job.is_finished = True
    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()

    department = Department()
    department.title = "ecobiolog"
    department.chief = 1
    department.members = '1, 3'
    department.email = "geoexplor@gmail.com"
    db_sess = db_session.create_session()
    db_sess.add(department)
    db_sess.commit()

    department = Department()
    department.title = "Бытовые задачи"
    department.chief = 3
    department.members = '3, 4'
    department.email = "VotEtoDa@gmail.com"
    db_sess = db_session.create_session()
    db_sess.add(department)
    db_sess.commit()

    #  app.run()


if __name__ == '__main__':
    main()

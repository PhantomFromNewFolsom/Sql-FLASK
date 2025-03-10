from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Job

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)

    user = User()
    user.name = "Scot"
    user.surname = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.name = "Alex"
    user.surname = "Pushkin"
    user.age = 19
    user.position = "boatswain"
    user.speciality = "ecobiolog"
    user.address = "module_1"
    user.email = "PushKing@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.name = "Adam"
    user.surname = "Smitt"
    user.age = 29
    user.position = "chef"
    user.speciality = "cook"
    user.address = "module_1"
    user.email = "galaktika@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.name = "Yop"
    user.surname = "Yan"
    user.age = 21
    user.position = "cabin boy"
    user.speciality = "doctor"
    user.address = "module_1"
    user.email = "ThisIsHorosho@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

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
    job.work_size = 24
    job.collaborators = "1, 2, 3"
    job.is_finished = True
    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()

    #  app.run()


if __name__ == '__main__':
    main()

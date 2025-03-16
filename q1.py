from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Job
from data.departments import Department

db = input()

global_init(f"db/{db}")
# global_init(db)
db_sess = create_session()
department = db_sess.query(Department).filter(Department.id == 1).first()
lst_id = [int(c) for c in department.members.split(', ')]
lst_jobs = []
jobs = db_sess.query(Job).filter(Job.work_size > 25).all()
users = db_sess.query(User).filter(User.id.in_(lst_id)).all()
for job in jobs:
    j = [int(c) for c in job.collaborators.split(', ')]
    for user in users:
        if user.id in j:
            print(user.surname, user.name)

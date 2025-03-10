from data import db_session
from data.users import User

db = input()

db_session.global_init(f"db/{db}")
db_sess = db_session.create_session()
users = db_sess.query(User).filter(User.address == 'module_1').all()
for user in users:
    print(user)

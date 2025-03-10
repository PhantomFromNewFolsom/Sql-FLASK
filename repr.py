from flask import Flask, render_template

from data.db_session import global_init, create_session
from data.jobs import Job

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

global_init(f'db/blogs.db')
db_sess = create_session()
lst = []
for job in db_sess.query(Job).all():
    lst.append(job)


@app.route('/table')
def table():
    global lst
    return render_template('table.html', title='Работа', list=lst)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

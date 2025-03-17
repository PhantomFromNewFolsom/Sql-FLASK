import flask
from flask import jsonify, make_response

from . import db_session
from .jobs import Job

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    news = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'user.name', 'user.surname', 'job', 'work_size',
                                    'start_date', 'end_date', 'is_finished'))
                 for item in news]
        }
    )


@blueprint.route('/api/jobs/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).get(news_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'user.name', 'user.surname', 'job', 'work_size',
                                       'start_date', 'end_date', 'is_finished'))
        }
    )

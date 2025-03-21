import datetime

import flask
from flask import jsonify, make_response, request

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


@blueprint.route('/api/jobs/<jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    try:
        jobs_id = int(jobs_id)
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 404)
    jobs = db_sess.query(Job).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'user.name', 'user.surname', 'job', 'work_size',
                                       'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    start_date = datetime.datetime(request.json['start_date'][0], request.json['start_date'][1],
                                   request.json['start_date'][2])
    end_date = datetime.datetime(request.json['end_date'][0], request.json['end_date'][1],
                                 request.json['end_date'][2])
    jobs = Job(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=start_date,
        end_date=end_date,
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()

    jobs = db_sess.query(Job).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

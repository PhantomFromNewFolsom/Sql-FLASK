from flask import Flask, jsonify
from flask_restful import abort, Api, Resource

from data import db_session

from .jobs import Job
from .job_parser import parser

app = Flask(__name__)
api = Api(app)


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('id', 'user.name', 'user.surname', 'job', 'work_size',
                  'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Job).all()
        return jsonify({'job': [item.to_dict(
            only=('id', 'user.name', 'user.surname', 'job', 'work_size',
                  'start_date', 'end_date', 'is_finished')) for item in job]})

    def post(self):
        args = parser.parse_args()
        print(args)
        session = db_session.create_session()
        job = Job(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})


def abort_if_job_not_found(job_id):
    try:
        job_id = int(job_id)
    except Exception:
        abort(400, message=f"Value Error: Job id is not int")
    session = db_session.create_session()
    job = session.query(Job).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")

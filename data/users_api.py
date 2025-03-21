import flask
from flask import jsonify, make_response, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<users_id>', methods=['GET'])
def get_one_user(users_id):
    db_sess = db_session.create_session()
    try:
        users_id = int(users_id)
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 404)
    users = db_sess.query(User).get(users_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                         'speciality', 'address', 'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<users_id>', methods=['DELETE'])
def delete_user(users_id):
    db_sess = db_session.create_session()
    try:
        jobs_id = int(users_id)
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 404)
    users = db_sess.query(User).get(jobs_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<users_id>', methods=['PUT'])
def edit_users(users_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    try:
        users_id = int(users_id)
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 404)
    users = db_sess.query(User).get(users_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    users.surname = request.json['surname']
    users.name = request.json['name']
    users.age = request.json['age']
    users.position = request.json['position']
    users.speciality = request.json['speciality']
    users.address = request.json['address']
    users.email = request.json['email']
    db_sess.commit()
    return jsonify({'success': 'OK'})
import flask
from flask import jsonify, request
from data import db_session
from data.users import User

blueprint = flask.Blueprint('UserApi', __name__, template_folder='templates')


@blueprint.route('/api/users/<string:email>/<string:password>')
def get_users_admin(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({'error': 'User not founded'})
    if not user.check_password(password):
        return jsonify({'error': "Passwords don't match"})
    if not user.status >= 1:
        return jsonify({'error': "You don't have permissions for this"})
    users = session.query(User).all()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'nickname', 'email', 'created_date', 'status',
                                    'background_image_id', 'publications', 'developers_diary', 'comments'))
                 for item in users]
        }
    )


@blueprint.route('/api/user/<string:email>/<string:password>', methods=['GET'])
def get_one_user(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({'error': 'Not found'})
    if not user.check_password(password):
        return jsonify({'error:' "Passwords don't match"})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'nickname', 'email', 'created_date', 'status',
                                       'background_image_id', 'publications', 'developers_diary', 'comments'))
        }
    )


@blueprint.route('/api/user/<string:email>/<string:password>/<int:user_id>', methods=['GET'])
def get_one_user_admin(email, password, user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({'error': 'Not found'})
    if not user.check_password(password):
        return jsonify({'error:' "Passwords don't match"})
    if not user.status >= 1:
        return jsonify({'error': "You don't have permissions for this"})
    user_find = session.query(User).get(user_id)
    if not user_find:
        return jsonify({'error': 'Not found'})
    if user_find.status > user.status:
        return jsonify({'error': "You don't have permissions for this"})
    return jsonify(
        {
            'user': user_find.to_dict(only=('id', 'surname', 'name', 'age', 'nickname', 'email', 'created_date',
                                            'status', 'background_image_id', 'publications', 'developers_diary',
                                            'comments'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'nickname', 'email', 'password']):
        return jsonify({'error': 'Missing some keys to create, you need keys to create:'
                                 'id, surname, name, age, nickname, email, password'})
    if session.query(User).get(request.json.get('id')):
        return jsonify({'error': 'Id already exists'})
    if session.query(User).filter(User.email == request.json.get('email')).first():
        return jsonify({'error': 'This email already exists'})
    if session.query(User).filter(User.nickname == request.json.get('nickname')).first():
        return jsonify({'error': 'This nickname already exists'})
    user = User()
    user.id = request.json.get('id')
    user.surname = request.json.get('surname')
    user.name = request.json.get('name')
    user.age = request.json.get('age')
    user.nickname = request.json.get('nickname')
    user.email = request.json.get('email')
    user.set_passwor(request.json.get('password'))
    user.background_image_id = 0
    user.status = 0
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<string:email>/<string:password>/<int:user_id>', methods=['DELETE'])
def delete_user_admin(email, password, user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({'error': 'Not found'})
    if not user.check_password(password):
        return jsonify({'error:' "Passwords don't match"})
    if not user.status >= 1:
        return jsonify({'error': "You don't have permissions for this"})
    user_find = session.query(User).get(user_id)
    if not user_find:
        return jsonify({'error': 'Not found'})
    if user_find.status > user.status:
        return jsonify({'error': "You don't have permissions for this"})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<string:email>/<string:password>', methods=['DELETE'])
def delete_user(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({'error': 'Not found'})
    if not user.check_password(password):
        return jsonify({'error:' "Passwords don't match"})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<string:email>/<string:password>/<int:user_id>', methods=['PUT'])
def put_user_admin(email, password, user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email)
    if not user:
        return jsonify({'error': 'Not found'})
    if not user.check_password(password):
        return jsonify({'error': "Passwords don't match"})
    if user.status < 1:
        return jsonify({'error': "You don't have permissions for this"})
    status = user.status
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    if len(request.json) == 0:
        return jsonify({'error': 'No keys for editing'})
    for key in request.json:
        if key not in ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from']:
            return jsonify({'error': 'Invalid key for editing'})
    if 'status' in request.json:
        status_2 = request.json.get('status')
        status_3 = user.status
        if status_2 < 0:
            return jsonify({'error': 'Invalid status'})
        if status < status_2 or status < status_3:
            return jsonify({'error': "You don't have permissions for this"})
    if 'email' in request.json:
        if session.query(User).filter(User.email == request.json.get('email')).first():
            return jsonify({'error': 'This email already exists'})
    if 'nickname' in request.json:
        if session.query(User).filter(User.nickname == request.json.get('nickname')).first():
            return jsonify({'error': 'This nickname already exists'})
    for key in request.json:
        if key == 'id':
            user.id = request.json.get(key)
        if key == 'surname':
            user.surname = request.json.get(key)
        if key == 'name':
            user.name = request.json.get(key)
        if key == 'age':
            user.age = request.json.get(key)
        if key == 'nickname':
            user.nickname = request.json.get(key)
        if key == 'background_image_id':
            user.background_image_id = request.json.get(key)
        if key == 'email':
            user.email = request.json.get(key)
        if key == 'password':
            user.set_password(password)
        if key == 'status':
            user.status = request.json.get(key)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<string:email>/<string:password>', methods=['PUT'])
def put_user(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email)
    if not user:
        return jsonify({'error': 'Not found'})
    if not user.check_password(password):
        return jsonify({'error': "Passwords don't match"})
    if len(request.json) == 0:
        return jsonify({'error': 'No keys for editing'})
    for key in request.json:
        if key not in ['id', 'surname', 'name', 'age', 'nickname', 'email', 'new_password',
                       'status', 'background_image_id']:
            return jsonify({'error': 'Invalid key for editing'})
    if 'nickname' in request.json:
        if session.query(User).filter(User.nickname == request.json.get('nickname')).first():
            return jsonify({'error': 'This nickname already exists'})
    if 'status' in request.json:
        return jsonify({'error': "You don't have permissions for this"})
    if 'email' in request.json:
        if session.query(User).filter(User.email == request.json.get('email')).first():
            return jsonify({'error': 'This email already exists'})
    for key in request.json:
        if key == 'id':
            user.id = request.json.get(key)
        if key == 'surname':
            user.surname = request.json.get(key)
        if key == 'name':
            user.name = request.json.get(key)
        if key == 'age':
            user.age = request.json.get(key)
        if key == 'nickname':
            user.nickname = request.json.get(key)
        if key == 'background_image_id':
            user.background_image_id = request.json.get(key)
        if key == 'email':
            user.email = request.json.get(key)
        if key == 'password':
            user.set_password(password)
    session.commit()
    return jsonify({'success': 'OK'})

from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.users import User
from data.UserApi.parser_user_api import parser
from data.UserApi.put_parser_user_api import put_parser
from data.UserApi.put_parser_user_admin_api import put_parser_admin


def check_admin(email, password, need_status=1):
    session = db_session.create_session()
    admin = session.query(User).filter(User.email == email).first()
    if not admin:
        abort(404, message=f"User {email} not found")
    if not admin.check_password(password):
        abort(404, message="Password don't match")
    if not admin.status >= need_status:
        abort(401, message="You don't have permissions for this")
    return admin, session


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user, session


def check_user(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        abort(404, message=f"User {email} not found")
    if not user.check_password(password):
        abort(404, message="Password don't match")
    return user, session


class UserResource(Resource):
    def get(self, email, password):
        user, session = check_user(email, password)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'nickname', 'status', 'background_image_id', 'email', 'publications',
                  'comments', 'created_date'))})

    def delete(self, email, password):
        user, session = check_user(email, password)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, email, password):
        user, session = check_user(email, password)
        args = put_parser.parse_args()
        for key in list(args.keys()):
            if args[key] is not None:
                if key == 'id':
                    if session.query(User).filter(User.nickname == args["id"]):
                        abort(400, message="This id already exists")
                    user.id = args['id']
                if key == 'surname':
                    user.surname = args['surname']
                if key == 'name':
                    user.name = args['name']
                if key == 'age':
                    print(args['age'])
                    user.age = args['age']
                if key == 'nickname':
                    if session.query(User).filter(User.nickname == args["nickname"]):
                        abort(400, message="This nickname already exists")
                    user.nickname = args['nickname']
                if key == 'background_image_id':
                    user.background_image_id = args['background_image_id']
                if key == 'email':
                    if session.query(User).filter(User.nickname == args["email"]):
                        abort(400, message="This email already exists")
                    user.email = args['email']
                if key == 'password':
                    user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResourceAdmin(Resource):
    def get(self, email, password):
        check_admin(email, password)
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'nickname', 'background_image_id', 'status', 'email',
                  'background_image_id', 'publications', 'developers_diary'))
            for item in users]})


class UserResourceAdmin(Resource):
    def get(self, email, password, user_id):
        check_admin(email, password)
        user, session = abort_if_user_not_found(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'nickname', 'status', 'background_image_id', 'email', 'publications',
                  'comments', 'created_date'))})

    def delete(self, email, password, user_id):
        check_admin(email, password)
        user, session = abort_if_user_not_found(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, email, password, user_id):
        admin, session_1 = check_admin(email, password)
        user, session = abort_if_user_not_found(user_id)
        args = put_parser_admin.parse_args()
        if args['status'] is not None:
            if args['status'] > admin.status:
                abort(401, message="You don't have permissions for this")
            if args['status'] < 0:
                abort(400, message="Invalid status")
        for key in list(args.keys()):
            if args[key] is not None:
                if key == 'id':
                    if session.query(User).filter(User.nickname == args["id"]):
                        abort(400, message="This id already exists")
                    user.id = args['id']
                if key == 'surname':
                    user.surname = args['surname']
                if key == 'name':
                    user.name = args['name']
                if key == 'age':
                    user.age = args['age']
                if key == 'nickname':
                    if session.query(User).filter(User.nickname == args["nickname"]):
                        abort(400, message="This nickname already exists")
                    user.nickname = args['nickname']
                if key == 'background_image_id':
                    user.background_image_id = args['background_image_id']
                if key == 'email':
                    if session.query(User).filter(User.nickname == args["email"]):
                        abort(400, message="This email already exists")
                    user.email = args['email']
                if key == 'status':
                    user.status = args['status']
                if key == 'password':
                    user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class CreateUserResource(Resource):
    def post(self):
        args = parser.parse_args()
        if not all(key in args for key in
                   ['id', 'surname', 'name', 'age', 'nickname', 'email', 'password']):
            return abort(400, message='Missing some keys to create, you need keys to create:'
                                      'id, surname, name, age, nickname, email, password')
        session = db_session.create_session()
        if session.query(User).get(args['id']):
            abort(400, message='Id already exists')
        if session.query(User).filter(User.email == args['email']).first():
            abort(400, message="This email already exists")
        if session.query(User).filter(User.email == args['nickname']).first():
            abort(400, message="This nickname already exists")
        user = User()
        user.id = args['id']
        user.name = args['name']
        user.surname = args['surname']
        user.age = args['age']
        user.nickname = args['nickname']
        user.status = 0
        user.email = args['email']
        user.background_image_id = 0
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

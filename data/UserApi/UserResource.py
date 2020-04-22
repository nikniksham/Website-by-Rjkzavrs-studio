import datetime
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.users import User
from data.UserApi.parser_user_api import parser
from data.UserApi.put_parser_user_api import put_parser
from data.UserApi.put_parser_user_admin_api import put_parser_admin


def raise_error(error):
    abort(400, message=error)


def check_password(password):
    errors = {0: 'Ok', 1: 'The password length must be 8 or more', 2: 'The password must contain at least 1 letter',
              3: 'The password must contain at least 1 digit'}
    if not len(password) >= 8:
        return False, errors[1]
    if password.isdigit():
        return False, errors[2]
    if password.isalpha():
        return False, errors[3]
    return True, errors[0]


def check_admin(email, password, need_status=1):
    session = db_session.create_session()
    admin = session.query(User).filter(User.email == email).first()
    if not admin:
        raise_error(f"User {email} not found")
    if not admin.check_password(password):
        raise_error("Password don't match")
    if admin.status < need_status:
        raise_error("You don't have permissions for this")
    return admin, session


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        raise_error(f"User {user_id} not found")
    return user, session


def check_user(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise_error(f"User {email} not found")
    if not user.check_password(password):
        raise_error("Password don't match")
    return user, session


class UserResource(Resource):
    def get(self, email, password):
        user, session = check_user(email, password)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'nickname', 'status', 'background_image_id', 'email', 'publications',
                  'comments', 'created_date'))})

    def delete(self, email, password):
        user, session = check_user(email, password)
        email = user.email
        session.delete(user)
        session.commit()
        return jsonify({'success': f'User {email} deleted'})

    def put(self, email, password):
        user, session = check_user(email, password)
        args = put_parser.parse_args()
        i = 0
        for key in list(args.keys()):
            if args[key] is not None:
                i += 1
                if key == 'id':
                    if session.query(User).filter(User.id == args["id"]).first():
                        raise_error("This ID already exists")
                    user.id = args['id']
                if key == 'surname':
                    user.surname = args['surname']
                if key == 'name':
                    user.name = args['name']
                if key == 'age':
                    user.age = args['age']
                if key == 'nickname':
                    if session.query(User).filter(User.nickname == args["nickname"]).first():
                        raise_error("This nickname already exists")
                    user.nickname = args['nickname']
                if key == 'background_image_id':
                    user.background_image_id = args['background_image_id']
                if key == 'email':
                    if session.query(User).filter(User.nickname == args["email"]).first():
                        raise_error("This email already exists")
                    user.email = args['email']
        session.commit()
        if i == 0:
            return raise_error('Empty edit request')
        return jsonify({'success': f'User {user.email} changed'})


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
        admin, session = check_admin(email, password)
        user, session = abort_if_user_not_found(user_id)
        if admin.status < user.status:
            raise_error("You don't have permissions for this")
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'nickname', 'status', 'background_image_id', 'email', 'publications',
                  'comments', 'created_date'))})

    def delete(self, email, password, user_id):
        admin, session = check_admin(email, password)
        user, session = abort_if_user_not_found(user_id)
        email = user.email
        if admin.status <= user.status:
            raise_error("You don't have permissions for this")
        session.delete(user)
        session.commit()
        return jsonify({'success': f'User {email} deleted'})

    def put(self, email, password, user_id):
        admin, session_1 = check_admin(email, password)
        user, session = abort_if_user_not_found(user_id)
        args = put_parser_admin.parse_args()
        if admin.status <= user.status:
            raise_error("You don't have permissions for this")
        if args['status'] is not None:
            if args['status'] > admin.status:
                raise_error("You don't have permissions for this")
            if args['status'] < 0:
                raise_error("Invalid status")
        i = 0
        for key in list(args.keys()):
            if args[key] is not None:
                i += 1
                if key == 'id':
                    if session.query(User).filter(User.id == args["id"]).first():
                        raise_error("This id already exists")
                    user.id = args['id']
                if key == 'surname':
                    user.surname = args['surname']
                if key == 'name':
                    user.name = args['name']
                if key == 'age':
                    user.age = args['age']
                if key == 'nickname':
                    if session.query(User).filter(User.nickname == args["nickname"]).first():
                        raise_error("This nickname already exists")
                    user.nickname = args['nickname']
                if key == 'background_image_id':
                    user.background_image_id = args['background_image_id']
                if key == 'email':
                    if session.query(User).filter(User.nickname == args["email"]).first():
                        raise_error("This email already exists")
                    user.email = args['email']
                if key == 'status':
                    user.status = args['status']
        session.commit()
        if i == 0:
            return raise_error('Empty edit request')
        return jsonify({'success': f'User {user.email} changed'})


class CreateUserResource(Resource):
    def post(self):
        args = parser.parse_args()
        if not all(key in args for key in
                   ['id', 'surname', 'name', 'age', 'nickname', 'email', 'password']):
            raise_error('Missing some keys to create, you need keys to create:'
                        'id, surname, name, age, nickname, email, password')
        session = db_session.create_session()
        if session.query(User).get(args['id']):
            raise_error('Id already exists')
        if session.query(User).filter(User.email == args['email']).first():
            raise_error("This email already exists")
        if session.query(User).filter(User.email == args['nickname']).first():
            raise_error("This nickname already exists")
        res = check_password(args['password'])
        if not res[0]:
            raise_error(res[1])
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
        user.created_date = datetime.datetime.now()
        session.add(user)
        session.commit()
        return jsonify({'success': f'User {args["email"]} created'})

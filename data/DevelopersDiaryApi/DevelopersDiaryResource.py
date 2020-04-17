import datetime

from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.developers_diary import DevelopersDiary
from data.DevelopersDiaryApi.put_parser_developers_diary_admin_api import put_parser_admin
from data.DevelopersDiaryApi.parser_developers_diary_api import parser
from data.users import User


def raise_error(error):
    abort(400, message=error)


def check_admin(email, password, accept_level=1):
    session = db_session.create_session()
    admin = session.query(User).filter(User.email == email).first()
    if not admin:
        raise_error('Admin not found')
    if not admin.check_password(password):
        raise_error("Passwords don't match")
    if admin.status < accept_level:
        raise_error("You don't have permissions for this")
    return admin, session


def check_user(email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise_error('User not found')
    if not user.check_password(password):
        raise_error("Passwords don't match")
    return user, session


def check_publication(publication_id, session, user=None):
    publication, accept_status = session.query(DevelopersDiary).get(publication_id), 1
    if not publication:
        raise_error('Publication not found')
    if user is not None:
        accept_status = user.status + 1
    if publication.availability_status > accept_status:
        raise_error("You don't have permissions for publication")
    return publication, session


class DevelopersDiaryResourceUser(Resource):
    def get(self, email, password, publication_id):
        user, session = check_user(email, password)
        publication = check_publication(publication_id, session, user)[0]
        return jsonify({'publication': publication.to_dict(
            only=('id', 'header', 'body', 'good_marks', 'bad_marks', 'created_date', 'comments', 'availability_status'
                  ))})

    def delete(self, email, password, publication_id):
        user, session = check_user(email, password)
        publication, session = check_publication(publication_id, session, user)
        session.delete(publication)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, email, password, publication_id):
        user, session = check_user(email, password)
        publication, session = check_publication(publication_id, session, user)
        args = put_parser_admin.parse_args()
        for key in list(args.keys()):
            if args[key] is not None:
                if key == 'id':
                    if session.query(DevelopersDiary).filter(DevelopersDiary.id == args["id"]):
                        raise_error("This id already exists")
                    publication.id = args['id']
                if key == 'header':
                    if session.query(DevelopersDiary).filter(DevelopersDiary.header == args["header"]):
                        raise_error("This header already exists")
                    publication.header = args['header']
                if key == 'body':
                    publication.body = args['body']
                if key == 'good_marks':
                    publication.good_marks = args['good_marks']
                if key == 'bad_marks':
                    publication.bad_marks = args['bad_marks']
                if key == 'availability_status':
                    publication.availability_status = args['availability_status']
        session.commit()
        return jsonify({'success': 'OK'})


class DevelopersDiaryListResourceAdmin(Resource):
    def get(self, email, password):
        check_admin(email, password)
        session = db_session.create_session()
        publications = session.query(DevelopersDiary).all()
        return jsonify({'publications': [item.to_dict(
            only=('id', 'header', 'body', 'good_marks', 'bad_marks', 'created_date', 'comments', 'availability_status',
                  'author_id'))
            for item in publications]})


class DevelopersDiaryResourceAdmin(Resource):
    def get(self, email, password, publication_id):
        admin, session = check_admin(email, password)
        publication, session = check_publication(publication_id, session, admin)
        return jsonify({'publication': publication.to_dict(
            only=('id', 'header', 'body', 'good_marks', 'bad_marks', 'created_date', 'comments', 'availability_status',
                  'author_id'))})

    def delete(self, email, password, publication_id):
        admin, session = check_admin(email, password)
        publication, session = check_publication(publication_id, session, admin)
        session.delete(publication)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, email, password, publication_id):
        admin, session = check_admin(email, password)
        publication, session = check_publication(publication_id, session, admin)
        args = put_parser_admin.parse_args()
        for key in list(args.keys()):
            if args[key] is not None:
                if key == 'id':
                    if session.query(DevelopersDiary).filter(DevelopersDiary.id == args["id"]):
                        raise_error("This id already exists")
                    publication.id = args['id']
                if key == 'header':
                    if session.query(DevelopersDiary).filter(DevelopersDiary.header == args["header"]):
                        raise_error("This header already exists")
                    publication.header = args['header']
                if key == 'body':
                    publication.body = args['body']
                if key == 'good_marks':
                    publication.good_marks = args['good_marks']
                if key == 'bad_marks':
                    publication.bad_marks = args['bad_marks']
                if key == 'availability_status':
                    publication.availability_status = args['availability_status']
        session.commit()
        return jsonify({'success': 'OK'})


class CreateDevelopersDiaryResource(Resource):
    def post(self, email, password):
        admin, session = check_admin(email, password)
        args = parser.parse_args()
        publication = DevelopersDiary()
        if session.query(DevelopersDiary).filter(DevelopersDiary.id == args["id"]).first():
            raise_error('This ID already exists')
        publication.id = args['id']
        if session.query(DevelopersDiary).filter(DevelopersDiary.header == args["header"]).first():
            raise_error('This Header already exists')
        publication.header = args['header']
        publication.body = args['body']
        publication.availability_status = args["availability_status"]
        publication.created_date = datetime.datetime.now()
        publication.good_marks = 0
        publication.bad_marks = 0
        admin.developers_diary.append(publication)
        session.merge(admin)
        session.commit()
        return jsonify({'success': 'OK'})

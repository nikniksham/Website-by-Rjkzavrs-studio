from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.DevelopersDiaryApi import DevelopersDiary


def abort_if_publication_not_found(developers_diary_publication_id):
    session = db_session.create_session()
    developers_diary_publication = session.query(DevelopersDiary).get(developers_diary_publication_id)
    if not developers_diary_publication:
        abort(404, message=f"DevelopersDiaryPublication {developers_diary_publication_id} not found")


class PublicationResource(Resource):
    def get(self, developers_diary_publication_id):
        abort_if_publication_not_found(developers_diary_publication_id)
        session = db_session.create_session()
        developers_diary_publication = session.query(DevelopersDiary).get(developers_diary_publication_id)
        return jsonify({'developers_diary_publication': developers_diary_publication.to_dict()})


class PublicationsResource(Resource):
    def get(self):
        session = db_session.create_session()
        developers_diary_publications = session.query(DevelopersDiary).all()
        return jsonify({'developers_diary_publications': developers_diary_publications})

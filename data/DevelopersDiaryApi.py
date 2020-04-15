import flask
from flask import jsonify
from data import db_session
from data.developers_diary import DevelopersDiary

blueprint = flask.Blueprint('DevelopersDiaryApi', __name__, template_folder='templates')


@blueprint.route('/api/get_publications')
def get_publications():
    session = db_session.create_session()
    developers_diary_publications = session.query(DevelopersDiary).all()
    return jsonify({'developers_diary_publications': developers_diary_publications})


@blueprint.route('/api/developers_diary_publication/<int:developers_diary_publication_id>',  methods=['GET'])
def get_one_publication(developers_diary_publication_id):
    session = db_session.create_session()
    developers_diary_publication = session.query(DevelopersDiary).get(developers_diary_publication_id)
    if not developers_diary_publication:
        return jsonify({'error': 'Not found'})
    return jsonify({'developers_diary_publication': developers_diary_publication.to_dict()})

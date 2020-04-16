import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class DevelopersDiary(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'developers_diary'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    header = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    good_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    bad_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    comments = orm.relation('Comments')
    availability_status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    author = orm.relation('User')

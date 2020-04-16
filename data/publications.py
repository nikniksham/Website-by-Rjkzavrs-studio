import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Publications(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'publications'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    header = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    good_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    bad_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    availability_status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    comments = orm.relation('Comments')
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    author = orm.relation('User')

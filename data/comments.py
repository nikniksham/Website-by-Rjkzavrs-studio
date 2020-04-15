import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    publication_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publications.id"))
    publication = orm.relation('Publications')
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    author = orm.relation('User')

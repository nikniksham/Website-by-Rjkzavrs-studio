import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    good_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    bad_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
    product = orm.relation('Products')
    developers_diary_publication_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("developers_diary.id"))
    developers_diary_publication = orm.relation('DevelopersDiary')
    publication_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publications.id"))
    publication = orm.relation('Publications')
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    author = orm.relation('User')

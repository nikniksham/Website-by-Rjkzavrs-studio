import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from datetime import datetime


class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
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

    def formatted_date(self):
        d = self.created_date
        return f"{str(d.year).rjust(2, '0')}.{str(d.month).rjust(2, '0')}.{d.day} {str(d.hour).rjust(2, '0')}:{str(d.minute).rjust(2, '0')}"

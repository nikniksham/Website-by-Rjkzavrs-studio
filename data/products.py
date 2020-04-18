import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Products(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    header = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.Binary, nullable=True)
    good_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    bad_marks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    quantity_in_stock = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    comments = orm.relation('Comments')

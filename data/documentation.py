import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Documentation(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'documentation'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    header = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    navigation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    availability_status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

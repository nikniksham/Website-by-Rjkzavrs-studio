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
    comments = orm.relation('Comments')
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    author = orm.relation('User')

    def formatted_date(self):
        d = self.created_date
        return f"{str(d.year).rjust(2, '0')}.{str(d.month).rjust(2, '0')}.{d.day} {str(d.hour).rjust(2, '0')}:{str(d.minute).rjust(2, '0')}"

import sqlalchemy

from .db_session import SqlAlchemyBase


class ChatMessages(SqlAlchemyBase):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(256))
    msg = sqlalchemy.Column(sqlalchemy.Text)

    def __repr__(self):
        return '<User %r>' % self.username

import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('jobs', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('departments', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('departments.id'))
)


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return self.__str__()

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.speciality"), nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer)
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    user = orm.relationship('User')

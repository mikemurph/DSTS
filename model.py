from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

#engine = path to our MySQL database
engine = create_engine("sqlite:///test.db.mwb")
Base = declarative_base()
Base.metadata.reflect(engine)

from sqlalchemy.orm import relationship, backref

#one of the existing tables in the temp MySQL is 'users'
class Users(Base):
    __table__ = Base.metadata.tables['users']


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessinomaker(bind=engine))
    for item in db_session.query(Users.id, Users.name):
        print(item)

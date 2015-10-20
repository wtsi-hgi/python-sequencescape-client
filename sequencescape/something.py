from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


global _engine


def connect(host, port, database, user, dialect='mysql'):
    db_url = '%s://%s:@%s:%s/%s' % (dialect, user, host, port, database)
    global _engine
    _engine = create_engine(db_url)


def get_session_instance():
    global _engine
    if not _engine:
        raise ConnectionError("Must connect database engine")
    Session = sessionmaker(bind=_engine)
    session = Session()
    return session


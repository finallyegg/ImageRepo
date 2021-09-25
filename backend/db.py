from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import current_app as app

engine = None
Session = None


@contextmanager
def read_only_session_scope():
    global engine
    global Session
    if engine is None:
        engine = create_engine(app.config["DATABASE_URI"], echo=False)
    if Session is None:
        Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@contextmanager
def session_scope():
    global engine
    global Session
    if engine is None:
        engine = create_engine(app.config["DATABASE_URI"], echo=False)
    if Session is None:
        Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

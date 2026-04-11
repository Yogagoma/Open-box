import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#Base for the models
class Base(DeclarativeBase):
    pass

#Sqlite engine 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL = f"sqlite:///{os.path.join(BASE_DIR, 'openbox.db')}"

engine = create_engine(URL, echo=True)

#Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

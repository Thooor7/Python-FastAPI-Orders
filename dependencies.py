from sqlalchemy.orm import sessionmaker
from models import db
def get_session():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()
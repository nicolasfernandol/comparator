from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# function to connect to the SQLite database
engine = create_engine('sqlite:///ingredients.db')
Session = sessionmaker(bind=engine)

# function to get a session
def get_session():
    return Session()
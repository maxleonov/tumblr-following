from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///tower.db', echo=False)
Session = sessionmaker(bind=engine)

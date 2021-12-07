import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(engine)

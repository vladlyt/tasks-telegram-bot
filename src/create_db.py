from sqlalchemy import create_engine
from src.models import User, Group, Task
from src.db import DATABASE_URL


def drop_db(engine=None):
    if engine is None:
        print("Connecting to the database...")
        engine = create_engine(DATABASE_URL)

    print("Dropping tables...")
    User.metadata.drop_all(engine)
    Group.metadata.drop_all(engine)
    Task.metadata.drop_all(engine)


def create_db(engine=None):
    if engine is None:
        print("Connecting to the database...")
        engine = create_engine(DATABASE_URL)

    print("Creating tables...")
    User.metadata.create_all(engine)
    Group.metadata.create_all(engine)
    Task.metadata.create_all(engine)


if __name__ == '__main__':
    print("Connecting to the database...")
    engine = create_engine(DATABASE_URL)
    drop_db(engine)
    create_db(engine)
    print("Done")

from sqlalchemy import create_engine
from src.models import User, Group, Task

if __name__ == '__main__':
    print("Connecting to the database...")
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

    print("Dropping tables...")
    User.metadata.drop_all(engine)
    Group.metadata.drop_all(engine)
    Task.metadata.drop_all(engine)

    print("Creating tables...")
    User.metadata.create_all(engine)
    Group.metadata.create_all(engine)
    Task.metadata.create_all(engine)

    print("Done")


import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    show_notifications = Column(Boolean, default=True)

    tasks = relationship(
        "Task", back_populates="user",
        cascade="all, delete",
        lazy='dynamic',
        passive_deletes=True,
    )
    groups = relationship(
        "Group", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f'User {self.id} with telegram id: {self.telegram_id}'


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    user = relationship('User', back_populates="groups")

    name = Column(String(32))

    tasks = relationship("Task", back_populates="group")

    def __repr__(self):
        return f'Group {self.name}'


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    user = relationship('User', back_populates="tasks")

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL'), nullable=True)
    group = relationship('Group', back_populates="tasks")

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    creation_date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    when_date = Column(Date, nullable=True)
    place = Column(String(128), nullable=True)

    def __repr__(self):
        return f'Task #{self.id}: {self.description[:20] if self.description else None}'

    def display(self):
        return (
            f'Title: {self.title}\n'
            f'Description: {self.description or "Empty"}\n'
            f'When date: {self.when_date.strftime("%d/%m/%Y") if self.when_date else "Empty"}\n'
            f'Place: {self.place or "Empty"}\n'
            f'Is Completed: {self.is_completed}'
        )

    def display_markdown(self):
        return (
            f'*Title*: {self.title}\n'
            f'*Description*: {self.description or "Empty"}\n'
            f'*When date*: {self.when_date.strftime("%d/%m/%Y") if self.when_date else "Empty"}\n'
            f'*Place*: {self.place or "Empty"}\n'
            f'{"*COMPLETED*" if self.is_completed else "*NOT COMPLETED*"}\n'
        )

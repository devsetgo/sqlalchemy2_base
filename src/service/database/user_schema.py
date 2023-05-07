# -*- coding: utf-8 -*-
from uuid import uuid4

from loguru import logger
from sqlalchemy import Boolean, Column, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property

from service.core.demo_user_generator import demo_creator
from service.database.common_schema import BaseModel, BaseDAO
from service.database.db_session import Base


class User(BaseModel, Base):
    """
    This class represents a user in the database and inherits from BaseModel and Base.

    It has three columns:
    1. id - Integer primary key (from base).
    2. first_name - String column for the user's first name.
    3. last_name - String column for the user's last name.
    4. full_name - Hybrid property that is calculated from the first and last name.

    Example usage:
        user = User(first_name="John", last_name="Doe")
        print(user.full_name) # "John Doe"
    """

    __tablename__ = "users"

    user_name = Column(String(50), unique=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(150), unique=True, index=True)
    notes = Column(String(5000))
    password = Column(String(50), index=True)
    is_active = Column(Boolean, default=False, index=True)
    is_approved = Column(Boolean, default=False, index=True)
    is_admin = Column(Boolean, default=False, index=True)

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}'"
            f")>"
        )


class UserDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, User)

    async def create_demo_user_data(self, num_instances=100):
        from tqdm import tqdm

        # Check if there are any existing users in the database
        filters = {"is_admin": False}
        existing_users = await self.list_all(filters=filters)
        if existing_users:
            logger.warning(
                "Demo data creation aborted. User table already has existing data."
            )
            return

        demo_users = demo_creator(num_instances)
        for values in tqdm(demo_users):
            # Create a new instance of the cls class with the generated values
            instance = self.clazz(id=str(uuid4()), **values)
            self.db.add(instance)

# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime
import datetime
from service.database.common_model import BaseModel
from service.database.db_session import Base
from sqlalchemy.ext.hybrid import hybrid_property
from loguru import logger
from service.database.db_session import db
from uuid import uuid4


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
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(150), unique=True)
    notes = Column(String(5000))
    password = Column(String(50))
    is_active = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

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

    @classmethod
    async def create_demo_data(cls, num_instances=10):
        import silly
        import random
        from service.core.user_lib import encrypt_pass
        import secrets

        start_date = datetime.datetime(2015, 8, 20)

        for i in range(num_instances):
            # Generate a random number of days between 0 and 365*50 (50 years)
            days_created = random.randint(0, 365 * 8)
            days_updated = random.randint(0, 365 * 8)

            # Add the random number of days to the start date to get the final datetime values
            date_created = start_date + datetime.timedelta(days=days_created)
            date_updated = start_date + datetime.timedelta(days=days_updated)

            values: dict = {
                "first_name": f"test-{secrets.token_hex(3)}",
                "last_name": f"test-{secrets.token_hex(3)}",
                "email": f"{secrets.token_hex(3)}@Example-{secrets.token_hex(1)}.com",
                "password": None,
                "is_admin": False,
                "date_created": date_created,
                "date_updated": date_updated,
            }

            pwd = secrets.token_hex(8)
            pwd_without_spaces = pwd.replace(" ", "")
            hash_pwd = encrypt_pass(pwd_without_spaces)
            values["password"] = hash_pwd

            # Create a new instance of the cls class with the generated values
            instance = cls(id=str(uuid4()), **values)

            # Call the create() method to add the instance to the database
            db.add(instance)

            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise

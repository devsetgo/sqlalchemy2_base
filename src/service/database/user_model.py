# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, DateTime, desc

# from service.database.common_model import BaseModel
from service.database.db_session import Base
from sqlalchemy.ext.hybrid import hybrid_property
from service.database.db_session import db
from uuid import uuid4
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import random
from service.core.user_lib import encrypt_pass
import secrets
from service.core.demo_user_generator import demo_creator


class User(Base):
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
    id = Column(String, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(150), unique=True)
    notes = Column(String(5000))
    password = Column(String(50))
    is_active = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    date_created = Column(DateTime, index=True, default=datetime.utcnow)
    date_updated = Column(
        DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )

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
    async def list_all(cls, filters=None, order_by=None):
        logger.debug(f"Listing all {cls.__name__} objects")
        query = select(cls)
        if filters:
            for key, value in filters.items():
                if key == "date_created":
                    query = query.where(cls.date_created >= value)
                elif key == "date_updated":
                    query = query.where(cls.date_updated >= value)
                else:
                    query = query.where(getattr(cls, key).like(f"%{value}%"))
        if order_by:
            column, direction = order_by.split(":")
            if direction.lower() == "desc":
                query = query.order_by(desc(getattr(cls, column)))
            else:
                query = query.order_by(getattr(cls, column))
        instances = await db.execute(query)
        instances = instances.scalars().all()
        return instances

    @classmethod
    async def create(cls, **kwargs):
        logger.debug(f"Creating {cls.__name__} with kwargs: {kwargs}")
        instance = cls(id=str(uuid4()), **kwargs)
        db.add(instance)

        try:
            await db.commit()
        except IntegrityError as e:
            logger.exception("Error committing to database")
            await db.rollback()
            raise ValueError("Duplicate value for unique field") from e
        except Exception as e:
            logger.exception("Error committing to database")
            await db.rollback()
            raise
        return instance

    @classmethod
    async def delete(cls, id):
        logger.debug(f"Deleting {cls.__name__} with ID {id}")
        query = cls.__table__.delete().where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception as e:
            logger.exception("Error committing to database")
            await db.rollback()
            raise

    @classmethod
    async def update(cls, id, **kwargs):
        logger.debug(f"Updating {cls.__name__} with ID {id} and kwargs: {kwargs}")
        query = (
            cls.__table__.update()
            .where(cls.id == bindparam("id"))
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        # Check if row exists before updating
        instance = await cls.get(id)

        await db.execute(query, {"id": id, **kwargs})
        # No need for try-except block here
        await db.commit()
        return instance

    @classmethod
    async def create_demo_user_data(cls, num_instances=100):
        from tqdm import tqdm
        
        # Check if there are any existing users in the database
        filters = {"is_admin": False}
        existing_users = await cls.list_all(filters=filters)
        if existing_users:
            logger.warning(
                "Demo data creation aborted. User table already has existing data."
            )
            return

        demo_users = demo_creator(num_instances)
        for values in tqdm(demo_users):
            # Create a new instance of the cls class with the generated values
            instance = cls(id=str(uuid4()), **values)
            db.add(instance)

            try:
                await db.commit()
            except Exception as e:
                logger.exception("Error committing demo data to database")
                await db.rollback()
                raise SQLAlchemyError(str(e))

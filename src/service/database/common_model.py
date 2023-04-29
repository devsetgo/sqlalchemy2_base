# -*- coding: utf-8 -*-
# from datetime import datetime
# from uuid import uuid4

# from sqlalchemy import Column, DateTime, String, desc
# from sqlalchemy.future import select
# from service.database.db_session import db
# from loguru import logger


# class BaseModel:
#     id = Column(String, primary_key=True)
#     date_created = Column(DateTime, index=True, default=datetime.utcnow)
#     date_updated = Column(
#         DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow
#     )

#     @classmethod
#     async def get(cls, id):
#         logger.debug(f"Getting {cls.__name__} with ID {id}")
#         query = select(cls).where(cls.id == id)
#         instances = await db.execute(query)
#         result = instances.first()
#         if result:
#             (instance,) = result
#             return instance
#         return None

#     @classmethod
#     async def create(cls, **kwargs):
#         logger.debug(f"Creating {cls.__name__} with kwargs: {kwargs}")
#         instance = cls(id=str(uuid4()), **kwargs)
#         db.add(instance)

#         try:
#             await db.commit()
#         except Exception as e:
#             logger.exception("Error committing to database")
#             await db.rollback()
#             raise
#         return instance

#     # @classmethod
#     # async def list_all(cls, filters=None, order_by=None):
#     #     logger.debug(f"Listing all {cls.__name__} objects")
#     #     query = select(cls)
#     #     if filters:
#     #         for key, value in filters.items():
#     #             if key == "date_created":
#     #                 query = query.where(cls.date_created >= value)
#     #             elif key == "date_updated":
#     #                 query = query.where(cls.date_updated >= value)
#     #             else:
#     #                 query = query.where(getattr(cls, key).like(f"%{value}%"))
#     #     if order_by:
#     #         column, direction = order_by.split(":")
#     #         if direction == "desc":
#     #             query = query.order_by(desc(getattr(cls, column)))
#     #         else:
#     #             query = query.order_by(getattr(cls, column))
#     #     instances = await db.execute(query)
#     #     instances = instances.scalars().all()
#     #     return instances

#     @classmethod
#     async def delete(cls, id):
#         logger.debug(f"Deleting {cls.__name__} with ID {id}")
#         query = cls.__table__.delete().where(cls.id == id)
#         await db.execute(query)
#         try:
#             await db.commit()
#         except Exception as e:
#             logger.exception("Error committing to database")
#             await db.rollback()
#             raise
#         return True

#     @classmethod
#     async def update(cls, id, **kwargs):
#         logger.debug(f"Updating {cls.__name__} with ID {id} and kwargs: {kwargs}")
#         query = (
#             cls.__table__.update()
#             .where(cls.id == id)
#             .values(**kwargs)
#             .execution_options(synchronize_session="fetch")
#         )

#         await db.execute(query)
#         try:
#             await db.commit()
#         except Exception as e:
#             logger.exception("Error committing to database")
#             await db.rollback()
#             raise
#         return await cls.get(id)

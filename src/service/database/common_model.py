from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.future import select


class BaseModel:
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    @classmethod
    async def create(cls, **kwargs):
        instance = cls(id=str(uuid4()), **kwargs)
        db.add(instance)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return instance

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            cls.__table__
            .update()
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return await cls.get(id)

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        instances = await db.execute(query)
        (instance,) = instances.first()
        return instance

    @classmethod
    async def get_all(cls):
        query = select(cls)
        instances = await db.execute(query)
        instances = instances.scalars().all()
        return instances

    @classmethod
    async def delete(cls, id):
        query = cls.__table__.delete().where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

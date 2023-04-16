from sqlalchemy import Column, String

from service.database.common_model import BaseModel
from service.database.db_session import Base

class User(BaseModel, Base):
    __tablename__ = "users"
    full_name = Column(String)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f")>"
        )

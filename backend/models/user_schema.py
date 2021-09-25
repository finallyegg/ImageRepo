from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum
from backend.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True)
    isAdmin = Column(Boolean, default=False, nullable=False)
    emailId = Column(String, nullable=True)


class UserDTO:
    def __init__(self, user_id, name, isAdmin):
        self.user_id = user_id
        self.name = name
        self.isAdmin = isAdmin

    def serialize(self):
        return {"id": self.user_id, "name": self.name, "isAdmin": self.isAdmin}

    @staticmethod
    def from_schema_object(user: User):
        return UserDTO(user.id, user.name, user.isAdmin)

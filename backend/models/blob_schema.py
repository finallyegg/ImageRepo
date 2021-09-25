from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum, JSON
from sqlalchemy.orm import relationship
from backend.models.base import Base
from backend.models.user_schema import User, UserDTO


class Blob(Base):
    __tablename__ = 'blobs'

    id = Column(String, primary_key=True)
    count = Column(Integer, nullable=False)


class BlobDTO:
    def __init__(self, id, count):
        self.id = id
        self.count = count

    def serialize(self):
        return {"id": self.id, "count": self.count}

    @staticmethod
    def from_schema_object(blob: Blob):
        return BlobDTO(blob.id, blob.count)

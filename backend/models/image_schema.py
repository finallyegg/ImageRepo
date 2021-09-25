from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum, JSON
from sqlalchemy.orm import relationship
from backend.models.base import Base
from backend.models.user_schema import User, UserDTO


class ImageChunk(Base):
    __tablename__ = 'imageChunks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', backref='imageChunks')
    pieceJSON = Column(JSON, nullable=False)  # pieces like blob + LRU
    locked = Column(Boolean, nullable=False)
    accessKey = Column(String)


class ImageChunkDTO:
    def __init__(self, image_chunk_id, name, creator, pieceJSON, locked, accessKey):
        self.image_chunk_id = image_chunk_id
        self.name = name
        self.creator = creator
        self.pieceJSON = pieceJSON
        self.locked = locked
        self.accessKey = accessKey

    def serialize(self, isCreator):
        d = {"id": self.image_chunk_id,
             "name": self.name,
             "creator": self.creator,
             "locked": self.locked}

        if isCreator:
            d["accessKey"] = self.accessKey
        return d

    @staticmethod
    def from_schema_object(image_chunk: ImageChunk):
        return ImageChunkDTO(image_chunk.id, image_chunk.name, image_chunk.creator_id, image_chunk.pieceJSON, image_chunk.locked, image_chunk.accessKey)

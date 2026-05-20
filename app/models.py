import uuid

from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String(255), nullable=False)
    content = Column(Text)

    owner_id = Column(
        String(36),
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class NoteShare(Base):
    __tablename__ = "note_shares"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    note_id = Column(
        String(36),
        ForeignKey("notes.id")
    )

    shared_with_id = Column(
        String(36),
        ForeignKey("users.id")
    )


class NoteVersion(Base):
    __tablename__ = "note_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    note_id = Column(
        String(36),
        ForeignKey("notes.id")
    )

    title = Column(String(255))
    content = Column(Text)

    version_number = Column(Integer)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
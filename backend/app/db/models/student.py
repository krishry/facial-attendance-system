
"""Student database model."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    student_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str] = mapped_column(
        String(100), nullable=False, default="Computer Science"
    )
    semester: Mapped[str] = mapped_column(
        String(20), nullable=False, default="1st"
    )
    section: Mapped[str] = mapped_column(
        String(20), nullable=False, default="A"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    face_embeddings = relationship(
        "FaceEmbedding",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    attendances = relationship(
        "Attendance",
        back_populates="student"
    )

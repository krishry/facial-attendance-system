
"""Attendance session database model."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    session_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )

    course_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    instructor_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    min_similarity_threshold: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    min_confirmations: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    attendances = relationship(
        "Attendance",
        back_populates="attendance_session"
    )

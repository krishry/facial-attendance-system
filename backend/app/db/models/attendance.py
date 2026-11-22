
"""Attendance record database model."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Attendance(Base):
    __tablename__ = "attendances"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "session_id",
            name="uq_student_session_attendance",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    session_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("attendance_sessions.session_id"),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    similarity_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="PRESENT"
    )

    is_live: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    liveness_score: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    student = relationship(
        "Student",
        back_populates="attendances",
    )

    attendance_session = relationship(
        "AttendanceSession",
        back_populates="attendances",
    )

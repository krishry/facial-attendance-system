
"""Initial schema: students, face_embeddings, attendances, attendance_sessions

Revision ID: a6b43ecaa6cb
Revises:
Create Date: 2026-09-13 00:49:20.315125
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a6b43ecaa6cb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 1. Students table
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("semester", sa.String(length=20), nullable=False),
        sa.Column("section", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_students_id", "students", ["id"], unique=False
    )
    op.create_index(
        "ix_students_student_id",
        "students",
        ["student_id"],
        unique=True,
    )

    # 2. Attendance sessions table
    op.create_table(
        "attendance_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=100), nullable=False),
        sa.Column("course_name", sa.String(length=100), nullable=True),
        sa.Column("instructor_name", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("min_similarity_threshold", sa.Float(), nullable=True),
        sa.Column("min_confirmations", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "closed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_attendance_sessions_id",
        "attendance_sessions",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_session_id",
        "attendance_sessions",
        ["session_id"],
        unique=True,
    )

    # 3. Face embeddings table
    op.create_table(
        "face_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("embedding", sa.LargeBinary(), nullable=False),
        sa.Column("model_name", sa.String(length=50), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_face_embeddings_id",
        "face_embeddings",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_face_embeddings_student_id",
        "face_embeddings",
        ["student_id"],
        unique=False,
    )

    # 4. Attendances table
    op.create_table(
        "attendances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=100), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("similarity_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("is_live", sa.Boolean(), nullable=False),
        sa.Column("liveness_score", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["attendance_sessions.session_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id",
            "session_id",
            name="uq_student_session_attendance",
        ),
    )

    op.create_index(
        "ix_attendances_id",
        "attendances",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_attendances_student_id",
        "attendances",
        ["student_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendances_session_id",
        "attendances",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:

    # Drop tables in reverse dependency order
    op.drop_index("ix_attendances_session_id", table_name="attendances")
    op.drop_index("ix_attendances_student_id", table_name="attendances")
    op.drop_index("ix_attendances_id", table_name="attendances")
    op.drop_table("attendances")

    op.drop_index(
        "ix_face_embeddings_student_id",
        table_name="face_embeddings",
    )
    op.drop_index("ix_face_embeddings_id", table_name="face_embeddings")
    op.drop_table("face_embeddings")

    op.drop_index(
        "ix_attendance_sessions_session_id",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_id",
        table_name="attendance_sessions",
    )
    op.drop_table("attendance_sessions")

    op.drop_index("ix_students_student_id", table_name="students")
    op.drop_index("ix_students_id", table_name="students")
    op.drop_table("students")

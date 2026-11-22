
"""Face embedding database model."""

import numpy as np

from sqlalchemy import Float, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    embedding: Mapped[bytes] = mapped_column(
        LargeBinary, nullable=False
    )

    model_name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    model_version: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    quality_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    student = relationship(
        "Student",
        back_populates="face_embeddings"
    )

    def set_vector(self, vector):
        """Convert a face embedding into binary float32 data."""
        vector_array = np.asarray(vector, dtype=np.float32)

        if vector_array.shape != (512,):
            raise ValueError(
                f"Expected a 512-dimensional vector, got {vector_array.shape}"
            )

        self.embedding = vector_array.tobytes()

    def get_vector(self):
        """Convert stored binary data back into a Python list."""
        if not self.embedding:
            return []

        return np.frombuffer(
            self.embedding,
            dtype=np.float32
        ).tolist()

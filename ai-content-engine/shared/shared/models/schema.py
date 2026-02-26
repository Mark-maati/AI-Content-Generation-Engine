"""OutputSchema model."""

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shared.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class OutputSchema(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "output_schemas"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="0.1.0")
    json_schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
    semantic_rules: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    quality_rules: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

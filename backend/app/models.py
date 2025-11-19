from datetime import datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    contact_number: Mapped[str] = mapped_column(nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    product_review: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("timezone('utc', now())"),
    )


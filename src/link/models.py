import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Link(Base):
    __tablename__="links"

    short_url: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    original_url: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text(
            "TIMEZONE('utc', now())")
    )
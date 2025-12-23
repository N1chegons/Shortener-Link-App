import datetime

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Link(Base):
    __tablename__="links"

    short_url: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    original_url: Mapped[str] = mapped_column(nullable=False)

    fav_by = relationship("FavoriteLink", back_populates="link")

    # created_at: Mapped[datetime.datetime] = mapped_column(
    #     server_default=text(
    #         "TIMEZONE('utc', now())")
    # )


class FavoriteLink(Base):
    __tablename__ = "favorite_links"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id:  Mapped[int] =  mapped_column(ForeignKey('users.id'), nullable=False)
    short_url:  Mapped[str] =  mapped_column(ForeignKey('links.short_url'), nullable=False)

    user = relationship("User", back_populates="favorite_links")
    link = relationship("Link", back_populates="fav_by")
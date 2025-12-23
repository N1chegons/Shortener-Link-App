import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict

from src.link.models import Link


class LinkView(BaseModel):
    original_url: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class FavoriteLinkView(BaseModel):
    id: int
    short_url: str

    # Вложенная схема для связанной ссылки
    link: Optional[LinkView] = None

    model_config = ConfigDict(from_attributes=True)

class FavoriteLinkViewForTest(FavoriteLinkView):
    user_id: int
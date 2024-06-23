from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

from utils.uuid import uuid_generator


class PageType(Enum):
    NotionPage = ("NOTION_PAGE",)
    WebPage = "WEB_PAGE"


class Page(SQLModel, table=True):
    id: str = Field(default_factory=uuid_generator, primary_key=True)
    title: Optional[str]
    url: str
    type: PageType

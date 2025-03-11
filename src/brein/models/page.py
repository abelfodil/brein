from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from brein.utils.uuid import uuid_generator


class PageType(Enum):
    NotionPage = ("NOTION_PAGE",)
    WebPage = "WEB_PAGE"


class Page(SQLModel, table=True):
    id: str = Field(default_factory=uuid_generator, index=True)
    title: Optional[str]
    url: str = Field(default=None, primary_key=True)
    type: PageType
    content: Optional["Content"] = Relationship(back_populates="page", sa_relationship_kwargs={"lazy": "joined"})  # type: ignore

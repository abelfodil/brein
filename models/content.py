from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

from utils.uuid import uuid_generator


class Content(SQLModel, table=True):
    id: str | None = Field(default_factory=uuid_generator, primary_key=True)
    page_id: str | None = Field(default=None, foreign_key="page.id")
    raw_content: str
    last_edit: datetime

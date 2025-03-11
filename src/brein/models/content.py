from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Session
from brein.models.page import Page
from brein.utils.uuid import uuid_generator


class Content(SQLModel, table=True):
    id: str | None = Field(default_factory=uuid_generator, primary_key=True)
    page_id: str | None = Field(default=None, unique=True, foreign_key="page.id")
    raw_content: str
    text: str | None
    last_edit: datetime = Field(default_factory=datetime.now)
    page: Page = Relationship(back_populates="content")

    @staticmethod
    def insert(engine, contents: "Content"):
        if len(contents) == 0:
            return []

        with Session(engine) as session:
            for content in contents:
                session.merge(content)
            session.commit()
            return contents

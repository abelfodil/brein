from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Session, select
from brein.models.page import Page
from brein.utils.uuid import uuid_generator


class TextContent(SQLModel, table=True):
    id: str | None = Field(default_factory=uuid_generator, primary_key=True)
    page_id: str | None = Field(default=None, unique=True, foreign_key="page.id")
    raw_content: str
    text: str | None
    last_edit: datetime = Field(default_factory=datetime.now)
    page: Page = Relationship(back_populates="text_content")

    @staticmethod
    def insert(engine, contents: "TextContent"):
        if len(contents) == 0:
            return []

        with Session(engine) as session:
            existing_contents = session.exec(
                select(TextContent).where(
                    TextContent.page_id.in_([c.page_id for c in contents])
                )
            ).all()
            existing_content_map = {c.page_id: c for c in existing_contents}

            for content in contents:
                if content.page_id in existing_content_map:
                    content.id = existing_content_map[content.page_id].id
                    session.merge(content)
                else:
                    session.add(content)

            session.commit()

            return contents

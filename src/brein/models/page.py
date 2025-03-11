from enum import Enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, Session, select
from brein.utils.uuid import uuid_generator


class PageType(Enum):
    NotionPage = ("NOTION_PAGE",)
    WebPage = "WEB_PAGE"


class Page(SQLModel, table=True):
    id: str = Field(default_factory=uuid_generator, index=True)
    title: Optional[str]
    url: str = Field(default=None, primary_key=True)
    type: PageType
    text_content: Optional["TextContent"] = Relationship(back_populates="page", sa_relationship_kwargs={"lazy": "joined"})  # type: ignore

    @staticmethod
    def get_all_pages(engine) -> List["Page"]:
        with Session(engine) as session:
            statement = select(Page)
            results = session.exec(statement)
            return results.all()

    @staticmethod
    def insert(engine, pages: List["Page"]) -> List["Page"]:
        if len(pages) == 0:
            return []

        with Session(engine) as session:
            existing_pages = session.exec(
                select(Page).where(Page.url.in_([p.url for p in pages]))
            ).all()
            existing_urls = {p.url for p in existing_pages}

            new_pages = []
            result = []
            for page in pages:
                if page.url in existing_urls:
                    existing_page = next(p for p in existing_pages if p.url == page.url)
                    result.append(existing_page)
                else:
                    new_pages.append(page)
                    result.append(page)

            if new_pages:
                session.add_all(new_pages)
                session.commit()

                new_page_ids = [p.id for p in new_pages]
                refetched_new_pages = session.exec(
                    select(Page).where(Page.id.in_(new_page_ids))
                ).all()

                refetched_dict = {p.id: p for p in refetched_new_pages}
                for i in range(len(result)):
                    if result[i].id in refetched_dict:
                        result[i] = refetched_dict[result[i].id]

            return result

from dataclasses import dataclass
from brein.connectors.notion import Notion
from brein.models.text_content import TextContent
from brein.tasks.ScrapeWebPageTask import ScrapeWebPageTask
from brein.tasks.Task import Task
from brein.models.page import Page, PageType
from brein.utils.log import log
from more_itertools import batched
from brein.tasks.TaskManager import task_manager
from brein.connectors.database import engine


@dataclass
class NotionSyncTask(Task[str]):
    def execute(self):
        try:
            notion_client = Notion(self.payload)
            page_or_content = notion_client.extract()

            for page_or_content_batch in batched(page_or_content, 10):
                page_batch = [
                    item for item in page_or_content_batch if isinstance(item, Page)
                ]
                page_batch = Page.insert(engine, page_batch)

                content_batch = [
                    item for item in page_or_content_batch if isinstance(item, TextContent)
                ]
                content_batch = TextContent.insert(engine, content_batch)

                web_pages = (
                    page for page in page_batch if page.type == PageType.WebPage
                )
                tasks = (ScrapeWebPageTask(payload=page) for page in web_pages)
                task_manager.add_tasks(tasks)
        except Exception as e:
            log.error(f"Task {self.id} execution failed: {str(e)}")
            raise  # Re-raise to trigger retry

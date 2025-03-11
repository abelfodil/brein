from brein.connectors.web import Web
from brein.models.text_content import TextContent
from brein.tasks.Task import Task
from brein.models.page import Page
from brein.utils.log import log
from brein.connectors.database import engine


class ScrapeWebPageTask(Task[Page]):
    def execute(self):
        try:
            content = Web.scrape_page(self.payload)
            if content is None:
                return

            TextContent.insert(engine, [content])
        except Exception as e:
            log.error(f"Task {self.id} execution failed: {str(e)}")
            raise  # Re-raise to trigger retry

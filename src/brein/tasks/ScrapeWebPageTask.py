from dataclasses import dataclass
from brein.connectors.web import Web
from brein.models.content import Content
from brein.tasks.Task import Task, TaskStatus
from brein.models.page import Page
from brein.utils.log import log
from brein.connectors.database import engine


class ScrapeWebPageTask(Task[Page]):
    def execute(self):
        self.update_status(TaskStatus.PROCESSING)

        try:
            content = Web.scrape_page(self.payload)
            if content is None:
                self.update_status(TaskStatus.SUCCESS)
                return

            Content.insert(engine, [content])

            self.update_status(TaskStatus.SUCCESS)
        except Exception as e:
            log.error(f"Task {self.id} execution failed: {str(e)}")
            raise  # Re-raise to trigger retry

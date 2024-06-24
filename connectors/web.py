from datetime import datetime
import urllib.request
from html2text import html2text
from models.content import Content
from models.page import Page, PageType
from utils.datetime import has_been_less_than, a_month_ago
from utils.log import log


class Web:
    def _extract_from_page(page: Page):
        if (
            not page
            or page.type != PageType.WebPage
            or (
                page.content and has_been_less_than(page.content.last_edit, a_month_ago)
            )
        ):
            return None

        page_name = page.title or page.url
        log.info(f'Fetching "{page_name}" web page.')

        try:
            raw_html = urllib.request.urlopen(page.url, timeout=30).read()
        except:
            log.warn(f'Could not fetch "{page_name}" web page.')
            return None

        try:
            text = html2text(raw_html)
        except:
            log.warn(f'Could not parse "{page_name}" web page.')
            text = None

        content = Content(page_id=page.id, raw_content=raw_html, text=text)
        if page.content:
            content.last_edit = datetime.now()
            content.id = page.content.id

        return content

    def extract(self, pages: list[Page]):
        contents = (Web._extract_from_page(page) for page in pages)
        contents = [content for content in contents if content]
        return contents

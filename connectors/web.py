from datetime import datetime
import urllib.request
from html2text import HTML2Text
from models.content import Content
from models.page import Page, PageType
from utils.datetime import has_been_less_than, a_month_ago
from utils.log import log


class Web:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0"
    }

    html2text = HTML2Text()

    def __init__(self):
        self.html2text.ignore_links = True
        self.html2text.escape_all = True

    def _extract_from_page(self, page: Page):
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

        request = urllib.request.Request(page.url, headers=Web.headers)
        try:
            raw_html = (
                urllib.request.urlopen(request, timeout=30).read().decode("utf-8")
            )
        except:
            log.warn(f'Could not fetch "{page_name}" web page.')
            return None

        try:
            text = self.html2text.handle(raw_html)
        except:
            log.warn(f'Could not parse "{page_name}" web page.')
            text = None

        content = Content(page_id=page.id, raw_content=raw_html, text=text)
        if page.content:
            content.last_edit = datetime.now()
            content.id = page.content.id

        return content

    def extract(self, pages: list[Page]):
        contents = (self._extract_from_page(page) for page in pages)
        contents = (content for content in contents if content)
        return contents

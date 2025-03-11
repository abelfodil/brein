from datetime import datetime
from io import StringIO
import urllib.request
from html2text import HTML2Text
from brein.models.content import Content
from brein.models.page import Page, PageType
from brein.utils.datetime import has_been_less_than, a_month_ago
from brein.utils.log import log
import gzip


class Web:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0"
    }

    html2text = HTML2Text()
    html2text.ignore_links = True
    html2text.escape_all = True

    def _extract_html(response) -> str:
        if response.info().get("Content-Encoding") == "gzip":
            buffer = StringIO(response.read())
            file = gzip.GzipFile(fileobj=buffer)
            data = file.read().decode("utf-8")
            return data
        else:
            return response.read().decode("utf-8")

    def _is_pdf(response):
        return response.getheader("Content-Type") == "application/pdf"

    def scrape_page(page: Page) -> Content:
        page_name = page.title or page.url

        if page.type != PageType.WebPage:
            raise Exception(f"Page {page_name} is not a web page.")

        if page.content and has_been_less_than(page.content.last_edit, a_month_ago):
            log.info(f"Skippping {page_name} since the content is too recent.")
            return None

        log.info(f'Fetching "{page_name}" web page.')

        request = urllib.request.Request(page.url, headers=Web.headers)
        try:
            response = urllib.request.urlopen(request, timeout=30)
            if Web._is_pdf(response):
                return None
            raw_html = Web._extract_html(response)
        except Exception as e:
            raise Exception(f'Could not fetch "{page_name}" web page. Error: {str(e)}.')

        try:
            text = Web.html2text.handle(raw_html)
        except Exception as e:
            raise Exception(f'Could not parse "{page_name}" web page. Error: {str(e)}.')

        content = Content(page_id=page.id, raw_content=raw_html, text=text)
        if page.content:
            content.last_edit = datetime.now()
            content.id = page.content.id

        return content

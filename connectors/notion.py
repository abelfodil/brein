from datetime import datetime
from models.content import Content
from notion_client import Client as NotionClient
from models.page import Page, PageType
from utils.dict import filter_keys, get_any_values, list_to_dict, recursive_get


class Notion:
    notion: NotionClient

    def __init__(self, notion_api_key):
        self.notion = NotionClient(auth=notion_api_key)

    def _adapt_page_to_model(notion_page):
        return Page(
            id=notion_page["id"],
            url=notion_page["url"],
            title=recursive_get(notion_page, ["plain_text"]),
            type=PageType.NotionPage,
        )

    def _extract_all_pages_recursively(self):
        results = self.notion.search()["results"]
        results = (filter_keys(page, ["url", "plain_text", "id"]) for page in results)
        results = [Notion._adapt_page_to_model(page) for page in results]
        return results

    def _extract_rich_content_or_default(block_content: dict):
        rich_content = recursive_get(block_content, ["rich_text"])
        return rich_content and list_to_dict(rich_content) or block_content

    def _extract_content_from_block(notion_block):
        block_content = Notion._extract_rich_content_or_default(notion_block)
        content = recursive_get(block_content, ["plain_text"])
        return content

    def _extract_url_from_block(notion_block):
        filtered_block = filter_keys(
            notion_block,
            ["bulleted_list_item", "embed", "file", "link_preview"],
        )

        block_content = Notion._extract_rich_content_or_default(filtered_block)

        return recursive_get(block_content, ["url"]) if block_content else None

    def _flatten_block_with_children(block):
        return [block, *(block.get("children") or [])]

    def _adapt_content_to_model(page: Page, notion_block):
        if (not notion_block) or notion_block["type"] in set(
            ["child_page", "heading_1", "heading_2", "heading_3"]
        ):
            return None

        url = Notion._extract_url_from_block(notion_block)
        content = Notion._extract_content_from_block(notion_block)

        return (
            Page(
                url=url,
                title=content,
                type=PageType.WebPage,
            )
            if url
            else content
            and Content(
                id=notion_block["id"],
                page_id=page.id,
                raw_content=content,
                last_edit=datetime.fromisoformat(notion_block["last_edited_time"]),
            )
        )

    def _extract_page_contents(self, page: Page):
        return self.notion.blocks.children.list(page.id)["results"]

    def _extract_content_from_pages(self, pages: list[Page]):
        contents = ((page, self._extract_page_contents(page)) for page in pages)
        contents = ((page, block) for page, blocks in contents for block in blocks)
        contents = (
            (page, flattened)
            for page, block in contents
            for flattened in Notion._flatten_block_with_children(block)
        )
        contents = (
            Notion._adapt_content_to_model(page, block) for page, block in contents
        )

        contents = [content for content in contents if content]
        return contents

    def extract(self):
        pages = self._extract_all_pages_recursively()
        contents = self._extract_content_from_pages(pages)
        return [*pages, *contents]

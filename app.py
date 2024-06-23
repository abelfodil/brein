import argparse
from connectors.notion import Notion
from connectors.database import create_db_and_tables, delete_db, persist_entities

parser = argparse.ArgumentParser(prog="brein", description="Second brain")

parser.add_argument("--notion_api_key")
parser.add_argument("--extract_from_notion", action="store_true")
parser.add_argument("--fresh_db", action="store_true")


def main():
    args = parser.parse_args()
    if args.fresh_db:
        delete_db()
    create_db_and_tables()
    if args.extract_from_notion:
        entities = Notion(args.notion_api_key).extract()
        persist_entities(entities)


if __name__ == "__main__":
    main()

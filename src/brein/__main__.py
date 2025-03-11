import argparse
from brein.connectors.database import (
    create_db_and_tables,
    delete_db,
)
from brein.tasks.NotionSyncTask import NotionSyncTask
from brein.tasks.TaskManager import task_manager

parser = argparse.ArgumentParser(prog="brein", description="Second brain")

parser.add_argument("--notion_api_key")
parser.add_argument("--fresh_db", action="store_true")


def main():
    args = parser.parse_args()
    if args.fresh_db:
        delete_db()
    create_db_and_tables()

    task_manager.add_tasks([NotionSyncTask(payload=args.notion_api_key)])
    task_manager.start_workers()

    while True:
        pass


if __name__ == "__main__":
    main()

import os
from sqlmodel import SQLModel, Session, create_engine, select
from more_itertools import batched
from brein.models.page import *
from brein.models.content import *

sqlite_file_name = "brein.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def delete_db():
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def read_all_values(model):
    with Session(engine) as session:
        statement = select(model)
        results = session.exec(statement)
        return results.all()


def persist_entities(entities):
    with Session(engine) as session:
        for entity_batch in batched(entities, 10):
            for entity in entity_batch:
                session.merge(entity)
            session.commit()

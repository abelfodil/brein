import os
from sqlmodel import SQLModel, Session, create_engine
from models.page import *
from models.content import *

sqlite_file_name = "brein.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def delete_db():
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def persist_entities(entities):
    with Session(engine) as session:
        for entity in entities:
            session.add(entity)
        session.commit()

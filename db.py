import os
from sqlmodel import SQLModel, create_engine, Session

db_url = os.getenv("DATABASE_URL")

if db_url is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(db_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
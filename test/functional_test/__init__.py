import os, contextlib
from icoin import core
from icoin.core.db import db
from icoin.core.config import DefaultConfig


def init():
    name = os.environ.get("DB_NAME", DefaultConfig.DB_NAME)
    os.environ["TESTING"] = "1"
    os.environ["DB_NAME"] = name + "_test"
    core.init()
    db.drop_all()
    db.create_all()

init()

def clean_db():
    "Truncates all tables in the database"
    # more efficient database-specific method could be implemented
    # for example using templates or rollback
    with contextlib.closing(db.engine.connect()) as conn:
        trans = conn.begin()
        
        tables = reversed(db.metadata.sorted_tables)
        for table in reversed(db.metadata.sorted_tables):
            conn.execute(table.delete())

        trans.commit()


from config import USED_DB
from services.databases.sqlite_db import SQLiteDB
from services.databases.mariadb_db import MariaDB

database = None

def DB():
    global database
    if database is None:
        database = DatabaseSelector(db_type=USED_DB)
    return database

class DatabaseSelector:
    def __init__(self, db_type="sqlite", **kwargs):
        if db_type == "sqlite":
            self.db = SQLiteDB(**kwargs)
        elif db_type == "mariadb":
            self.db = MariaDB(**kwargs)
        else:
            raise ValueError(f"Unknown database type: {db_type}")

    def __getattr__(self, name):
        # Forward any method calls to the chosen DB
        return getattr(self.db, name)

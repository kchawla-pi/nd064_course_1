import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

NUM_CONNECTION = 0


@dataclass
class ConnectionManager:
    db_path: Path
    _count: int = 0

    def _increment(self):
        self._count += 1

    @contextmanager
    def connect(self):
        with sqlite3.connect(self.db_path) as connection:
            self._increment()
            connection.row_factory = sqlite3.Row
            yield connection


@contextmanager
def yield_db_connection(db_path='database.db'):
    """
    Function to get a database connection.
    This function connects to database with the name `database.db`
    """
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        yield connection

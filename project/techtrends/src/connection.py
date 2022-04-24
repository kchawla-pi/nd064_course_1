import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DBConnectionManager:
    db_path: Path
    _count: int = 0

    @property
    def count(self):
        return self._count

    def _increment(self):
        self._count += 1

    @contextmanager
    def connect(self):
        with sqlite3.connect(self.db_path) as connection:
            self._increment()
            connection.row_factory = sqlite3.Row
            yield connection

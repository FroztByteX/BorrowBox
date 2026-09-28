import sqlite3
from pathlib import Path


class Database:
    def __init__(self, database_path: str | Path = "database/borrowBox.db"):
        self.database_path = Path(database_path)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def create_tables(self) -> None:
        with self.connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS equipments(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    quantity INTEGER NOT NULL,
                    available INTEGER NOT NULL
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS borrowers(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    contact VARCHAR(50) NOT NULL
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS borrow_records(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    borrower_id INTEGER NOT NULL,
                    equipment_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    date_borrowed TEXT NOT NULL,
                    date_returned TEXT,
                    status VARCHAR(20) NOT NULL,

                    FOREIGN KEY (borrower_id)
                        REFERENCES borrowers(id),

                    FOREIGN KEY (equipment_id)
                        REFERENCES equipments(id)
                )
                """
            )
from database.database import Database

from .model import Borrower, BorrowRecord


class BorrowingRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_borrower(self, borrower: Borrower) -> Borrower:
        with self.database.connect() as con:
            cursor = con.execute(
                "INSERT INTO borrowers(name, contact) VALUES (?, ?)",
                (borrower.name, borrower.contact)
            )
            borrower.id = cursor.lastrowid
        return borrower

    def find_borrower(self, name: str, contact: str) -> Borrower | None:
        with self.database.connect() as con:
            row = con.execute(
                """
                SELECT id, name, contact FROM borrowers
                WHERE LOWER(name) = LOWER(?) AND contact = ?
                """,
                (name, contact)
            ).fetchone()

        if row is None:
            return None

        return Borrower(id=row[0], name=row[1], contact=row[2])

    def list_borrowers(self) -> list[Borrower]:
        with self.database.connect() as con:
            rows = con.execute(
                "SELECT id, name, contact FROM borrowers ORDER BY id"
            ).fetchall()

        return [Borrower(id=row[0], name=row[1], contact=row[2]) for row in rows]

    def add(self, record: BorrowRecord) -> BorrowRecord:
        with self.database.connect() as con:
            cursor = con.execute(
                """
                INSERT INTO borrow_records(borrower_id, equipment_id, 
                    quantity, date_borrowed, date_returned, status) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (record.borrower_id, record.equipment_id, record.quantity,
                    record.date_borrowed, record.date_returned, record.status)
            )
            record.id = cursor.lastrowid
        return record

    def list(self) -> list[BorrowRecord]:
        with self.database.connect() as con:
            rows = con.execute(
                """
                SELECT id, borrower_id, equipment_id, quantity, date_borrowed, date_returned, status 
                FROM borrow_records ORDER BY id
                """
            ).fetchall()

        return [
            BorrowRecord(
                id=row[0], borrower_id=row[1], equipment_id=row[2], quantity=row[3],
                date_borrowed=row[4], date_returned=row[5], status=row[6]
            )
            for row in rows
        ]
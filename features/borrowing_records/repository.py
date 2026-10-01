from database.database import Database

from .model import BorrowingRecord


class BorrowingRecordsRepository:
    def __init__(self, database: Database):
        self.database = database

    def list(self, status: str = "All") -> list[BorrowingRecord]:
        with self.database.connect() as con:
            if status == "All":
                rows = con.execute(
                    """
                    SELECT id, borrower_id, equipment_id, quantity, date_borrowed, date_returned, status
                    FROM borrow_records ORDER BY id DESC
                    """
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, borrower_id, equipment_id, quantity, date_borrowed, date_returned, status
                    FROM borrow_records WHERE status = ? ORDER BY id DESC
                    """,
                    (status,)
                ).fetchall()

        return [
            BorrowingRecord(
                id=row[0], borrower_id=row[1], equipment_id=row[2], quantity=row[3],
                date_borrowed=row[4], date_returned=row[5], status=row[6]
            )
            for row in rows
        ]
from datetime import datetime, timezone

from database.database import Database

from .model import Borrower, BorrowRecord
from .repository import BorrowingRepository


class EquipmentBorrowingService:
    def __init__(self, database: Database):
        self.database = database
        self.repository = BorrowingRepository(database)

    def get_or_create_borrower(self, borrower: Borrower) -> Borrower:
        existing_borrower = self.repository.find_borrower(borrower.name, borrower.contact)
        if existing_borrower is not None:
            return existing_borrower

        return self.repository.add_borrower(borrower)

    def add_borrower(self, borrower: Borrower) -> Borrower:
        return self.get_or_create_borrower(borrower)

    def get_borrowers(self) -> list[Borrower]:
        return self.repository.list_borrowers()

    def borrow_equipment(self,borrower_id: int,equipment_id: int, quantity: int) -> BorrowRecord:
        if quantity <= 0:
            raise ValueError("Borrow quantity must be greater than zero.")

        with self.database.connect() as con:
            equipment = con.execute(
                "SELECT quantity, available FROM equipments WHERE id = ?",
                (equipment_id,)
            ).fetchone()

            if equipment is None:
                raise ValueError("Equipment was not found.")

            available = equipment[1]

            if quantity > available:
                raise ValueError("Not enough equipment available.")

            borrower = con.execute(
                "SELECT id FROM borrowers WHERE id = ?",
                (borrower_id,)
            ).fetchone()

            if borrower is None:
                raise ValueError("Borrower was not found.")

            date_borrowed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

            cursor = con.execute(
                """
                INSERT INTO borrow_records(
                    borrower_id, equipment_id, quantity, date_borrowed, status) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (borrower_id, equipment_id, quantity, date_borrowed, "Borrowed")
            )

            con.execute(
                "UPDATE equipments SET available = available - ? WHERE id = ?",
                (quantity,equipment_id)
            )
            record_id = cursor.lastrowid

        return BorrowRecord(
            id=record_id,
            borrower_id=borrower_id,
            equipment_id=equipment_id,
            quantity=quantity,
            date_borrowed=date_borrowed,
            status="Borrowed"
        )

    def get_borrow_records(self) -> list[BorrowRecord]:
        return self.repository.list()
from database.database import Database


class EquipmentReturnRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_transaction(self, transaction_id: int):
        with self.database.connect() as con:
            return con.execute(
                "SELECT id, equipment_id, quantity, status FROM borrow_records WHERE id = ?",
                (transaction_id,)
            ).fetchone()

    def get_transaction_details(self, transaction_id: int):
        with self.database.connect() as con:
            return con.execute(
                """
                SELECT br.id, b.id, b.name, e.id, e.name, br.quantity, br.date_borrowed, br.date_returned, br.status
                FROM borrow_records br
                JOIN borrowers b ON br.borrower_id = b.id
                JOIN equipments e ON br.equipment_id = e.id
                WHERE br.id = ?
                """,
                (transaction_id,)
            ).fetchone()

    def get_active_transactions(self):
        with self.database.connect() as con:
            return con.execute(
                """
                SELECT br.id, b.name, e.name, br.quantity FROM borrow_records br
                JOIN borrowers b ON br.borrower_id = b.id
                JOIN equipments e ON br.equipment_id = e.id
                WHERE br.status = 'Borrowed' ORDER BY br.id
                """
            ).fetchall()

    def return_transaction(self, transaction_id: int, date_returned: str) -> None:
        with self.database.connect() as con:
            con.execute(
                "UPDATE borrow_records SET date_returned = ?, status = ? WHERE id = ?",
                (date_returned, "Returned", transaction_id)
            )
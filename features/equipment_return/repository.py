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

    def return_transaction(self, transaction_id: int, date_returned: str) -> None:
        with self.database.connect() as con:
            con.execute(
                "UPDATE borrow_records SET date_returned = ?, status = ? WHERE id = ?",
                (date_returned, "Returned", transaction_id)
            )
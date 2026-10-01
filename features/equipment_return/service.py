from datetime import datetime

from database.database import Database

from .repository import EquipmentReturnRepository


class EquipmentReturnService:
    def __init__(self, database: Database):
        self.database = database
        self.repository = EquipmentReturnRepository(database)

    def return_equipment(self, transaction_id: int) -> None:
        transaction = self.repository.get_transaction(transaction_id)

        if transaction is None:
            raise ValueError("Transaction was not found.")

        equipment_id = transaction[1]
        quantity = transaction[2]
        status = transaction[3]

        if status == "Returned":
            raise ValueError("This equipment has already been returned.")

        date_returned = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.database.connect() as con:
            con.execute(
                "UPDATE borrow_records SET date_returned = ?, status = ? WHERE id = ?",
                (date_returned, "Returned", transaction_id)
            )
            con.execute(
                "UPDATE equipments SET available = available + ? WHERE id = ?",
                (quantity, equipment_id)
            )
from datetime import datetime

from database.database import Database

from .model import EquipmentReturn
from .repository import EquipmentReturnRepository


class EquipmentReturnService:
    def __init__(self, database: Database):
        self.database = database
        self.repository = EquipmentReturnRepository(database)

    def get_active_transactions(self):
        return self.repository.get_active_transactions()

    def return_equipment(self, transaction_id: int) -> EquipmentReturn:
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

        receipt = self.repository.get_transaction_details(transaction_id)

        if receipt is None:
            raise ValueError("Unable to retrieve transaction details for the receipt.")

        return EquipmentReturn(
            transaction_id=receipt[0],
            borrower_id=receipt[1],
            borrower_name=receipt[2],
            equipment_id=receipt[3],
            equipment_name=receipt[4],
            quantity=receipt[5],
            date_borrowed=receipt[6],
            date_returned=receipt[7],
            status=receipt[8]
        )
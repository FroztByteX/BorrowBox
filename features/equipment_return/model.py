from dataclasses import dataclass


@dataclass
class EquipmentReturn:
    transaction_id: int
    borrower_id: int
    borrower_name: str
    equipment_id: int
    equipment_name: str
    quantity: int
    date_borrowed: str
    date_returned: str
    status: str
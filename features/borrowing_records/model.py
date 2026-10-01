from dataclasses import dataclass


@dataclass
class BorrowingRecord:
    id: int
    borrower_id: int
    equipment_id: int
    quantity: int
    date_borrowed: str
    date_returned: str | None
    status: str
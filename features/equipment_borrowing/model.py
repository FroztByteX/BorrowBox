from dataclasses import dataclass


@dataclass
class Borrower:
    name: str
    contact: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.contact = self.contact.strip()

        if not self.name:
            raise ValueError("Borrower name must not be empty")

        if not self.contact:
            raise ValueError("Borrower contact must not be empty")


@dataclass
class BorrowRecord:
    borrower_id: int
    equipment_id: int
    quantity: int
    date_borrowed: str
    status: str = "Borrowed"
    date_returned: str | None = None
    id: int | None = None
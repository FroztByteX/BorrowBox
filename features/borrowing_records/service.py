from database.database import Database

from .model import BorrowingRecord
from .repository import BorrowingRecordsRepository


class BorrowingRecordsService:
    def __init__(self, database: Database):
        self.repository = BorrowingRecordsRepository(database)

    def get_records(self, status: str = "All") -> list[BorrowingRecord]:
        return self.repository.list(status)
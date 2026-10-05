from database.database import Database

from .model import Dashboard
from .repository import DashboardRepository


class DashboardService:
    def __init__(self, database: Database):
        self.repository = DashboardRepository(database)

    def get_statistics(self) -> Dashboard:
        return self.repository.get_statistics()

    def get_borrowing_by_category(self) -> list[tuple]:
        return self.repository.get_borrowing_by_category()

    def get_most_borrowed_equipment(self) -> list[tuple]:
        return self.repository.get_most_borrowed_equipment()
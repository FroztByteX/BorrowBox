from database.database import Database

from .model import EquipmentSearchResult
from .repository import EquipmentSearchRepository


class EquipmentSearchService:
    def __init__(self, database: Database):
        self.repository = EquipmentSearchRepository(database)

    def search_equipment(self, keyword: str) -> list[EquipmentSearchResult]:
        return self.repository.search(keyword)
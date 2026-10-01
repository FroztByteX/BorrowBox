from database.database import Database

from .model import EquipmentSearchResult


class EquipmentSearchRepository:
    def __init__(self, database: Database):
        self.database = database

    def search(self, keyword: str) -> list[EquipmentSearchResult]:
        keyword = keyword.strip()
        with self.database.connect() as con:
            rows = con.execute(
                """SELECT id, name, category, quantity, available FROM equipments
                WHERE CAST(id AS TEXT) LIKE ? OR name LIKE ? OR category LIKE ? OR CAST(available AS TEXT) LIKE ?
                ORDER BY id
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            ).fetchall()

        return [EquipmentSearchResult(id=row[0], name=row[1], category=row[2], quantity=row[3], available=row[4])
            for row in rows
        ]
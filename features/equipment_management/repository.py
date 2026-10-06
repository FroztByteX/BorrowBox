from database.database import Database

from .model import Equipment


class EquipmentRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, equipment: Equipment) -> Equipment:
        with self.database.connect() as con:
            cursor = con.execute(
                """
                INSERT INTO equipments(
                    name,
                    category,
                    quantity,
                    available
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    equipment.name,
                    equipment.category,
                    equipment.quantity,
                    equipment.available
                )
            )

            equipment.id = cursor.lastrowid

        return equipment

    def list(self) -> list[Equipment]:
        with self.database.connect() as con:
            rows = con.execute(
                "SELECT * FROM equipments"
            ).fetchall()

        return [
            Equipment(
                id=row[0],
                name=row[1],
                category=row[2],
                quantity=row[3],
                available=row[4]
            )
            for row in rows
        ]

    def get(self, equipment_id: int) -> Equipment | None:
        with self.database.connect() as con:
            row = con.execute(
                "SELECT * FROM equipments WHERE id = ?",
                (equipment_id,)
            ).fetchone()

        if row is None:
            return None

        return Equipment(
            id=row[0],
            name=row[1],
            category=row[2],
            quantity=row[3],
            available=row[4]
        )

    def exists(
        self,
        name: str,
        category: str,
        equipment_id: int | None = None
    ) -> bool:
        with self.database.connect() as con:

            if equipment_id is None:
                row = con.execute(
                    """
                    SELECT id
                    FROM equipments
                    WHERE LOWER(name) = LOWER(?)
                    AND LOWER(category) = LOWER(?)
                    """,
                    (name, category)
                ).fetchone()

            else:
                row = con.execute(
                    """
                    SELECT id
                    FROM equipments
                    WHERE LOWER(name) = LOWER(?)
                    AND LOWER(category) = LOWER(?)
                    AND id != ?
                    """,
                    (name, category, equipment_id)
                ).fetchone()

        return row is not None

    def update(self, equipment: Equipment) -> Equipment:
        with self.database.connect() as con:
            con.execute(
                """
                UPDATE equipments
                SET name = ?,
                    category = ?,
                    quantity = ?,
                    available = ?
                WHERE id = ?
                """,
                (
                    equipment.name,
                    equipment.category,
                    equipment.quantity,
                    equipment.available,
                    equipment.id
                )
            )

        return equipment

    def has_active_borrowing(self, equipment_id: int) -> bool:
        with self.database.connect() as con:
            row = con.execute(
                "SELECT EXISTS(SELECT 1 FROM borrow_records WHERE equipment_id = ? AND status = 'Borrowed')",
                (equipment_id,)
            ).fetchone()

        return bool(row[0])

    def delete(self, equipment_id: int) -> None:
        with self.database.connect() as con:
            con.execute(
                "DELETE FROM equipments WHERE id = ?",
                (equipment_id,)
            )
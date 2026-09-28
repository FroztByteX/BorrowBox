from database.database import Database
from .model import Equipment
from .repository import EquipmentRepository


class EquipmentManagementService:
    def __init__(self, database: Database):
        self.repository = EquipmentRepository(database)

    def add_equipment(self, equipment: Equipment) -> Equipment:
        if self.repository.exists(equipment.name, equipment.category):
            raise ValueError("Equipment already exists.")

        return self.repository.add(equipment)

    def get_equipment(self) -> list[Equipment]:
        return self.repository.list()

    def get_equipment_by_id(self, equipment_id: int) -> Equipment | None:
        return self.repository.get(equipment_id)

    def update_equipment(self, equipment: Equipment) -> Equipment:
        if self.repository.exists(equipment.name, equipment.category, equipment.id):
            raise ValueError("Another equipment with the same name and category already exists.")

        return self.repository.update(equipment)

    def delete_equipment(self, equipment_id: int) -> None:
        self.repository.delete(equipment_id)

import sys

from PyQt6.QtWidgets import QApplication

from database.database import Database
from features.equipment_management.repository import EquipmentRepository
from features.equipment_management.service import EquipmentManagementService
from features.equipment_management.view import EquipmentManagementView


def main():
    database = Database()
    database.create_tables()

    repository = EquipmentRepository(database)
    service = EquipmentManagementService(database)

    app = QApplication(sys.argv)

    window = EquipmentManagementView(service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

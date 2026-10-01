import sys

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from database.database import Database
from features.borrowing_records.service import BorrowingRecordsService
from features.borrowing_records.view import BorrowingRecordsView
from features.equipment_borrowing.service import EquipmentBorrowingService
from features.equipment_borrowing.view import EquipmentBorrowingView
from features.equipment_management.service import EquipmentManagementService
from features.equipment_management.view import EquipmentManagementView
from features.equipment_return.service import EquipmentReturnService
from features.equipment_return.view import EquipmentReturnView
from features.search_equipment.service import EquipmentSearchService
from features.search_equipment.view import EquipmentSearchView


class BorrowBoxWindow(QMainWindow):
    def __init__(self, equipment_management, equipment_borrowing, equipment_return,
        borrowing_records, search_equipment):
        super().__init__()
        self.equipment_management = equipment_management
        self.equipment_borrowing = equipment_borrowing
        self.equipment_return = equipment_return
        self.borrowing_records = borrowing_records
        self.search_equipment = search_equipment

        self.setWindowTitle("BorrowBox")
        self.resize(1100, 650)
        self.build_ui()

    def build_ui(self) -> None:
        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(14)

        header = QWidget()
        header_layout = QHBoxLayout(header)

        title_group = QVBoxLayout()
        title = QLabel("BorrowBox")
        title.setObjectName("appTitle")
        subtitle = QLabel("Equipment Borrowing and Tracking Management System")
        subtitle.setObjectName("appSubtitle")
        title_group.addWidget(title)
        title_group.addWidget(subtitle)
        header_layout.addLayout(title_group)
        layout.addWidget(header)

        tabs = QTabWidget()
        tabs.addTab(self.equipment_management, "Equipments")
        tabs.addTab(self.equipment_borrowing, "Borrow Equipment")
        tabs.addTab(self.equipment_return, "Return Equipment")
        tabs.addTab(self.borrowing_records, "Borrowing Records")
        tabs.addTab(self.search_equipment, "Search Equipment")
        layout.addWidget(tabs)

        self.tabs = tabs
        self.tabs.currentChanged.connect(self.refresh_current_page)

    def refresh_current_page(self, index: int) -> None:
        current_page = self.tabs.widget(index)

        if hasattr(current_page, "refresh"):
            current_page.refresh()

        if hasattr(current_page, "search_equipment"):
            current_page.search_equipment()


def main():
    database = Database()
    database.create_tables()

    equipment_management = EquipmentManagementService(database)
    equipment_borrowing = EquipmentBorrowingService(database)
    equipment_return = EquipmentReturnService(database)
    borrowing_records = BorrowingRecordsService(database)
    search_equipment = EquipmentSearchService(database)

    app = QApplication(sys.argv)

    equipment_management_view = EquipmentManagementView(equipment_management)
    equipment_borrowing_view = EquipmentBorrowingView(equipment_borrowing, equipment_management)
    equipment_return_view = EquipmentReturnView(equipment_return)
    borrowing_records_view = BorrowingRecordsView(borrowing_records)
    search_equipment_view = EquipmentSearchView(search_equipment)

    window = BorrowBoxWindow(
        equipment_management_view, equipment_borrowing_view, equipment_return_view,
        borrowing_records_view, search_equipment_view
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
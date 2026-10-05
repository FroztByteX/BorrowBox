from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .service import EquipmentSearchService


class SortableTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other) -> bool:
        self_value = self.data(Qt.ItemDataRole.UserRole)
        other_value = other.data(Qt.ItemDataRole.UserRole)

        if self_value is not None and other_value is not None:
            try:
                return self_value > other_value
            except ValueError:
                pass

        return super().__lt__(other)


class EquipmentSearchView(QWidget):
    def __init__(self, service: EquipmentSearchService):
        super().__init__()
        self.service = service
        self.build_ui()
        self.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())
        self.search_equipment()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Search by ID, name, category, or availability")

        search_button = QPushButton("Search")
        search_button.setObjectName("primaryButton")
        search_button.clicked.connect(self.search_equipment)
        self.search_input.returnPressed.connect(self.search_equipment)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget(0, 6)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(["ID", "Equipment Name", "Category", "Quantity", "Available", "Status"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

    def search_equipment(self) -> None:
        keyword = self.search_input.text()
        equipments = self.service.search_equipment(keyword)

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(equipments))

        for row, equipment in enumerate(equipments):
            if equipment.available > 0:
                status = "Available"
            else:
                status = "Unavailable"

            values = [f"EQ-{equipment.id:03d}", equipment.name, equipment.category, equipment.quantity, equipment.available, status]
            sort_values = [equipment.id, equipment.name, equipment.category, equipment.quantity, equipment.available, status]

            for column, value in enumerate(values):
                item = SortableTableWidgetItem(str(value))
                item.setData(Qt.ItemDataRole.UserRole, sort_values[column])

                self.table.setItem(row, column, item)

        self.table.setSortingEnabled(True)
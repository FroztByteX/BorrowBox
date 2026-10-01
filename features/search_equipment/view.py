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


class EquipmentSearchView(QWidget):
    def __init__(self, service: EquipmentSearchService):
        super().__init__()
        self.service = service
        self.build_ui()
        self.search_equipment()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, name, category, or availability")

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_equipment)
        self.search_input.returnPressed.connect(self.search_equipment)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Equipment Name", "Category", "Quantity", "Available", "Status"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def search_equipment(self) -> None:
        keyword = self.search_input.text()
        equipments = self.service.search_equipment(keyword)
        self.table.setRowCount(len(equipments))

        for row, equipment in enumerate(equipments):
            if equipment.available > 0:
                status = "Available"
            else:
                status = "Unavailable"

            values = [f"EQ-{equipment.id:03d}", equipment.name, equipment.category,
                equipment.quantity, equipment.available, status
            ]

            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
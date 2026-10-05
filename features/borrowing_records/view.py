from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .service import BorrowingRecordsService


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


class BorrowingRecordsView(QWidget):
    def __init__(self, service: BorrowingRecordsService):
        super().__init__()
        self.service = service
        self.build_ui()
        self.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        filter_layout = QHBoxLayout()

        self.status_filter = QComboBox()
        self.status_filter.setObjectName("formCombo")
        self.status_filter.addItems(["All", "Borrowed", "Returned"])
        self.status_filter.currentTextChanged.connect(self.refresh)
        filter_layout.addWidget(self.status_filter)
        layout.addLayout(filter_layout)

        self.table = QTableWidget(0, 7)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "Transaction ID", "Borrower ID", "Equipment ID",
            "Quantity", "Date Borrowed", "Date Returned", "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

    def refresh(self) -> None:
        status = self.status_filter.currentText()
        records = self.service.get_records(status)

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            values = [
                f"BTR-{record.id:03d}",
                f"BID-{record.borrower_id:03d}",
                f"EQ-{record.equipment_id:03d}",
                record.quantity, record.date_borrowed, record.date_returned or "", record.status
            ]

            sort_values = [
                record.id, record.borrower_id, record.equipment_id, record.quantity, record.date_borrowed, record.date_returned or "", record.status
            ]

            for column, value in enumerate(values):
                item = SortableTableWidgetItem(str(value))
                item.setData(Qt.ItemDataRole.UserRole, sort_values[column])

                self.table.setItem(row, column, item)

        self.table.setSortingEnabled(True)
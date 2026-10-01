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


class BorrowingRecordsView(QWidget):
    def __init__(self, service: BorrowingRecordsService):
        super().__init__()
        self.service = service
        self.build_ui()
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        filter_layout = QHBoxLayout()

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Borrowed", "Returned"])
        self.status_filter.currentTextChanged.connect(self.refresh)
        filter_layout.addWidget(self.status_filter)
        layout.addLayout(filter_layout)

        self.table = QTableWidget(0, 7)

        self.table.setHorizontalHeaderLabels([
            "Transaction ID", "Borrower ID", "Equipment ID",
            "Quantity", "Date Borrowed", "Date Returned", "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def refresh(self) -> None:
        status = self.status_filter.currentText()
        records = self.service.get_records(status)
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            values = [
                f"BTR-{record.id:03d}",
                f"BID-{record.borrower_id:03d}",
                f"EQ{record.equipment_id:03d}",
                record.quantity, record.date_borrowed,
                record.date_returned or "",
                record.status
            ]

            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
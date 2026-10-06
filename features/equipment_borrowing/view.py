from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from features.equipment_management.service import EquipmentManagementService

from .model import Borrower
from .service import EquipmentBorrowingService


class EquipmentBorrowingView(QWidget):
    def __init__(self, service: EquipmentBorrowingService, equipment_service: EquipmentManagementService, refresh_callback=None):
        super().__init__()
        self.service = service
        self.equipment_service = equipment_service
        self.refresh_callback = refresh_callback
        self.build_ui()
        self.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.borrower_input = QComboBox()
        self.borrower_input.setObjectName("formCombo")
        self.borrower_input.currentIndexChanged.connect(self.borrower_selection_changed)
        form.addRow("Borrower", self.borrower_input)

        self.name_label = QLabel("Borrower Name")
        self.name_input = QLineEdit()
        self.name_input.setObjectName("formInput")
        form.addRow(self.name_label, self.name_input)

        self.contact_label = QLabel("Borrower Contact")
        self.contact_input = QLineEdit()
        self.contact_input.setObjectName("formInput")
        self.contact_input.setPlaceholderText("e.g., 09*********")
        form.addRow(self.contact_label, self.contact_input)

        self.equipment_input = QComboBox()
        self.equipment_input.setObjectName("formCombo")
        form.addRow("Equipment", self.equipment_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setObjectName("formInput")
        form.addRow("Quantity", self.quantity_input)
        layout.addLayout(form)

        borrow_button = QPushButton("Borrow Equipment")
        borrow_button.setObjectName("primaryButton")
        borrow_button.clicked.connect(self.borrow_equipment)
        layout.addWidget(borrow_button)

        self.table = QTableWidget(0, 7)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "Transaction ID", "Borrower ID", "Equipment ID",
            "Quantity", "Date Borrowed", "Date Returned", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        self.borrower_selection_changed()

    def refresh(self) -> None:
        self.refresh_borrowers()
        self.refresh_equipment()
        self.refresh_records()

    def refresh_borrowers(self) -> None:
        current_borrower_id = self.borrower_input.currentData(Qt.ItemDataRole.UserRole)
        self.borrower_input.blockSignals(True)
        self.borrower_input.clear()
        self.borrower_input.addItem("+ Add New Borrower", None)

        borrowers = self.service.get_borrowers()
        selected_index = 0

        for borrower in borrowers:
            self.borrower_input.addItem(f"BID-{borrower.id:03d} | {borrower.name} | {borrower.contact}", borrower.id)
            if borrower.id == current_borrower_id:
                selected_index = (self.borrower_input.count() - 1)

        self.borrower_input.setCurrentIndex(selected_index)
        self.borrower_input.blockSignals(False)
        self.borrower_selection_changed()

    def refresh_equipment(self) -> None:
        current_equipment_id = self.equipment_input.currentData(Qt.ItemDataRole.UserRole)
        self.equipment_input.clear()

        equipments = self.equipment_service.get_equipment()
        selected_index = -1

        for equipment in equipments:
            if equipment.available <= 0:
                continue

            self.equipment_input.addItem(
                f"EQ-{equipment.id:03d} | "
                f"{equipment.name} | "
                f"Available: {equipment.available}",
                equipment.id
            )

            if equipment.id == current_equipment_id:
                selected_index = self.equipment_input.count() - 1

        if self.equipment_input.count() == 0:
            self.equipment_input.addItem("No equipment available", None)
        elif selected_index >= 0:
            self.equipment_input.setCurrentIndex(selected_index)

    def borrower_selection_changed(self) -> None:
        is_new_borrower = self.borrower_input.currentData(Qt.ItemDataRole.UserRole) is None

        self.name_label.setVisible(is_new_borrower)
        self.name_input.setVisible(is_new_borrower)
        self.contact_label.setVisible(is_new_borrower)
        self.contact_input.setVisible(is_new_borrower)

    def borrow_equipment(self) -> None:
        borrower_id = self.borrower_input.currentData(Qt.ItemDataRole.UserRole)

        try:
            equipment_id = self.equipment_input.currentData(Qt.ItemDataRole.UserRole)
            if equipment_id is None:
                raise ValueError("Please select an available equipment.")

            quantity = int(self.quantity_input.text())

            if quantity <= 0:
                raise ValueError("Borrow quantity must be greater than zero.")

            equipment = self.equipment_service.get_equipment_by_id(equipment_id)

            if equipment is None:
                raise ValueError("Equipment was not found.")

            if quantity > equipment.available:
                raise ValueError("Not enough equipment available.")

            if borrower_id is None:
                borrower = Borrower(self.name_input.text(), self.contact_input.text())
                borrower = self.service.get_or_create_borrower(borrower)
                borrower_id = borrower.id

            record = self.service.borrow_equipment(borrower_id, equipment_id, quantity)

        except ValueError as error:
            QMessageBox.warning(self,"Invalid Borrowing", str(error))
            return

        QMessageBox.information(self,"Borrowing Successful",f"Transaction BTR-{record.id:03d} created successfully.")

        self.clear_inputs()
        self.refresh()
        if self.refresh_callback:
            self.refresh_callback()

    def clear_inputs(self) -> None:
        self.borrower_input.setCurrentIndex(0)
        self.name_input.clear()
        self.contact_input.clear()
        self.quantity_input.clear()

    def refresh_records(self) -> None:
        records = (self.service.get_borrow_records())
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            values = [f"BTR-{record.id:03d}", f"BID-{record.borrower_id:03d}", f"EQ-{record.equipment_id:03d}",
                record.quantity, record.date_borrowed, record.date_returned or "", record.status
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, record.id)

                self.table.setItem(row, column, item)
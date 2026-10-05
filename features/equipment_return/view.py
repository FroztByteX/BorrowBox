from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .service import EquipmentReturnService


class EquipmentReturnView(QWidget):
    def __init__(self, service: EquipmentReturnService):
        super().__init__()
        self.service = service
        self.build_ui()
        self.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.transaction_input = QComboBox()
        self.transaction_input.setObjectName("formCombo")
        form.addRow("Transaction ID", self.transaction_input)
        layout.addLayout(form)

        return_button = QPushButton("Return Equipment")
        return_button.setObjectName("primaryButton")
        return_button.clicked.connect(self.return_equipment)
        layout.addWidget(return_button)

        receipt_box = QGroupBox("Return Receipt")
        receipt_box.setObjectName("receiptBox")
        receipt_layout = QFormLayout(receipt_box)
        self.transaction_label = QLabel("-")
        self.borrower_id_label = QLabel("-")
        self.borrower_name_label = QLabel("-")
        self.equipment_id_label = QLabel("-")
        self.equipment_name_label = QLabel("-")
        self.quantity_label = QLabel("-")
        self.date_borrowed_label = QLabel("-")
        self.date_returned_label = QLabel("-")
        self.status_label = QLabel("-")

        receipt_layout.addRow("Transaction ID:", self.transaction_label)
        receipt_layout.addRow("Borrower ID:", self.borrower_id_label)
        receipt_layout.addRow("Borrower Name:", self.borrower_name_label)
        receipt_layout.addRow("Equipment ID:", self.equipment_id_label)
        receipt_layout.addRow("Equipment Name:", self.equipment_name_label)
        receipt_layout.addRow("Quantity:", self.quantity_label)
        receipt_layout.addRow("Date Borrowed:", self.date_borrowed_label)
        receipt_layout.addRow("Date Returned:", self.date_returned_label)
        receipt_layout.addRow("Status:", self.status_label)
        layout.addWidget(receipt_box)

        self.clear_receipt()

    def refresh(self) -> None:
        current_transaction_id = self.transaction_input.currentData(Qt.ItemDataRole.UserRole)

        self.transaction_input.blockSignals(True)
        self.transaction_input.clear()

        transactions = self.service.get_active_transactions()
        for transaction in transactions:
            transaction_id, borrower_name, equipment_name, quantity = transaction
            display_text = f"BTR-{transaction_id} | {borrower_name} | {equipment_name} | Qty: {quantity}"
            self.transaction_input.addItem(display_text, transaction_id)

        if current_transaction_id is not None:
            index = self.transaction_input.findData(current_transaction_id, Qt.ItemDataRole.UserRole)
            if index >= 0:
                self.transaction_input.setCurrentIndex(index)

        self.transaction_input.blockSignals(False)

        if self.transaction_input.count() == 0:
            self.transaction_input.addItem("No active transactions available", None)

    def return_equipment(self) -> None:
        transaction_id = self.transaction_input.currentData(Qt.ItemDataRole.UserRole)
        if transaction_id is None:
            QMessageBox.warning(self, "Invalid Return", "Please select an active transaction to return.")
            return

        try:
            receipt = self.service.return_equipment(transaction_id)

        except ValueError as error:
            QMessageBox.warning(self, "Invalid Return", str(error))
            return

        self.display_receipt(receipt)

        QMessageBox.information(self, "Return Successful", "Equipment returned successfully.\n\n"
                                f"Transaction BTR-{receipt.transaction_id:03d} has been marked as returned.")

        self.refresh()

    def display_receipt(self, receipt) -> None:
        self.transaction_label.setText(f"BTR-{receipt.transaction_id:03d}")
        self.borrower_id_label.setText(f"BID-{receipt.borrower_id:03d}")
        self.borrower_name_label.setText(receipt.borrower_name)
        self.equipment_id_label.setText(f"EQ-{receipt.equipment_id:03d}")
        self.equipment_name_label.setText(receipt.equipment_name)
        self.quantity_label.setText(str(receipt.quantity))
        self.date_borrowed_label.setText(receipt.date_borrowed)
        self.date_returned_label.setText(receipt.date_returned)
        self.status_label.setText(receipt.status)

    def clear_receipt(self) -> None:
        self.transaction_label.setText("-")
        self.borrower_id_label.setText("-")
        self.borrower_name_label.setText("-")
        self.equipment_id_label.setText("-")
        self.equipment_name_label.setText("-")
        self.quantity_label.setText("-")
        self.date_borrowed_label.setText("-")
        self.date_returned_label.setText("-")
        self.status_label.setText("-")
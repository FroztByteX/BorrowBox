from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .service import EquipmentReturnService


class EquipmentReturnView(QWidget):
    def __init__(self, service: EquipmentReturnService, refresh_callback=None):
        super().__init__()
        self.service = service
        self.refresh_callback = refresh_callback
        self.latest_receipt = None
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

        self.view_receipt_button = QPushButton("View Latest Receipt")
        self.view_receipt_button.setObjectName("secondaryButton")
        self.view_receipt_button.setEnabled(False)
        self.view_receipt_button.clicked.connect(self.open_latest_receipt)
        layout.addWidget(self.view_receipt_button)

        layout.addStretch()

    def refresh(self) -> None:
        current_transaction_id = self.transaction_input.currentData(Qt.ItemDataRole.UserRole)

        self.transaction_input.blockSignals(True)
        self.transaction_input.clear()

        transactions = self.service.get_active_transactions()
        for transaction in transactions:
            transaction_id, borrower_name, equipment_name, quantity = transaction

            display_text = f"BTR-{transaction_id:03d} | {borrower_name} | {equipment_name} | Qty: {quantity}"
            self.transaction_input.addItem(display_text, transaction_id)

        if current_transaction_id is not None:
            index = self.transaction_input.findData(current_transaction_id, Qt.ItemDataRole.UserRole)
            if index >= 0:
                self.transaction_input.setCurrentIndex(index)

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

        self.latest_receipt = receipt
        self.view_receipt_button.setEnabled(True)
        self.refresh()
        if self.refresh_callback:
            self.refresh_callback()

        self.open_latest_receipt()

    def open_latest_receipt(self) -> None:
        if self.latest_receipt is None:
            QMessageBox.information(self, "No Receipt Available", "Complete an equipment return first.")
            return

        receipt = self.latest_receipt

        dialog = QDialog(self)
        dialog.setWindowTitle("BorrowBox - Return Receipt")
        dialog.setMinimumWidth(440)
        dialog.setModal(True)

        dialog_layout = QVBoxLayout(dialog)

        receipt_box = QGroupBox()
        receipt_box.setObjectName("receiptBox")
        receipt_layout = QVBoxLayout(receipt_box)

        heading = QLabel("Return Receipt")
        heading.setObjectName("receiptTitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(heading)

        receipt_form = QFormLayout()

        fields = [
            ("Transaction ID:", f"BTR-{receipt.transaction_id:03d}"),
            ("Borrower ID:", f"BID-{receipt.borrower_id:03d}"),
            ("Borrower Name:", receipt.borrower_name),
            ("Equipment ID:", f"EQ-{receipt.equipment_id:03d}"),
            ("Equipment Name:", receipt.equipment_name),
            ("Quantity:", str(receipt.quantity)),
            ("Date Borrowed:", receipt.date_borrowed),
            ("Date Returned:", receipt.date_returned),
            ("Status:", receipt.status),
        ]

        for field_name, field_value in fields:
            value_label = QLabel(field_value)
            value_label.setWordWrap(True)
            receipt_form.addRow(field_name, value_label)

        receipt_layout.addLayout(receipt_form)
        dialog_layout.addWidget(receipt_box)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("Close")
        close_button.setObjectName("primaryButton")
        close_button.clicked.connect(dialog.accept)
        button_layout.addWidget(close_button)

        dialog_layout.addLayout(button_layout)

        dialog.exec()
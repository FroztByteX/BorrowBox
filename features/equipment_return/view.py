from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
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

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.transaction_input = QLineEdit()
        self.transaction_input.setPlaceholderText("Example: BTR-001")
        form.addRow("Transaction ID", self.transaction_input)
        layout.addLayout(form)

        return_button = QPushButton("Return Equipment")
        return_button.clicked.connect(self.return_equipment)
        layout.addWidget(return_button)

    def return_equipment(self) -> None:
        try:
            transaction_text = self.transaction_input.text().strip().upper()
            transaction_text = transaction_text.removeprefix("BTR-")
            transaction_id = int(transaction_text)
            self.service.return_equipment(transaction_id)

        except ValueError as error:
            QMessageBox.warning(self, "Invalid Return", str(error))
            return

        QMessageBox.information(self, "Return Successful", "Equipment returned successfully.")

        self.transaction_input.clear()
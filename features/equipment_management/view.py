from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
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

from .model import Equipment
from .service import EquipmentManagementService


class SortableTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other) -> bool:
        self_value = self.data(Qt.ItemDataRole.UserRole)
        other_value = other.data(Qt.ItemDataRole.UserRole)

        if self_value is not None and other_value is not None:
            try:
                return self_value > other_value
            except TypeError:
                pass

        return super().__lt__(other)


class EquipmentManagementView(QWidget):
    def __init__(self, service: EquipmentManagementService):
        super().__init__()
        self.service = service
        self.selected_equipment_id = None
        self.build_ui()
        self.setStyleSheet(Path(__file__).with_name("style.qss").read_text())
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setObjectName("formInput")
        self.category_input = QLineEdit()
        self.category_input.setObjectName("formInput")
        self.quantity_input = QLineEdit()
        self.quantity_input.setObjectName("formInput")

        name_label = QLabel("Equipment Name")
        name_label.setObjectName("formLabel")

        category_label = QLabel("Category")
        category_label.setObjectName("formLabel")

        quantity_label = QLabel("Quantity")
        quantity_label.setObjectName("formLabel")

        form.addRow(name_label, self.name_input)
        form.addRow(category_label, self.category_input)
        form.addRow(quantity_label, self.quantity_input)
        layout.addLayout(form)

        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Equipment")
        add_button.setObjectName("addButton")
        add_button.clicked.connect(self.add_equipment)
        button_layout.addWidget(add_button)

        update_button = QPushButton("Update Equipment")
        update_button.setObjectName("updateButton")
        update_button.clicked.connect(self.update_equipment)
        button_layout.addWidget(update_button)

        delete_button = QPushButton("Delete Equipment")
        delete_button.setObjectName("deleteButton")
        delete_button.clicked.connect(self.delete_equipment)
        button_layout.addWidget(delete_button)

        clear_button = QPushButton("Clear Inputs")
        clear_button.setObjectName("clearButton")
        clear_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.table = QTableWidget(0, 5)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(["ID","Equipment Name","Category","Quantity","Available"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.cellClicked.connect(self.select_equipment)
        layout.addWidget(self.table)

    def add_equipment(self) -> None:
        try:
            equipment = Equipment(self.name_input.text(), self.category_input.text(), self.quantity_input.text())
            self.service.add_equipment(equipment)

        except ValueError as error:
            QMessageBox.warning(self,"Invalid Equipment",str(error))
            return

        QMessageBox.information(self,"Adding Success",f"Equipment is added successfully.")
        self.clear_inputs()
        self.refresh()

    def select_equipment(self,row: int,column: int) -> None:
        item = self.table.item(row,0)

        if item is None:
            return

        equipment_id = item.data(Qt.ItemDataRole.UserRole)
        equipment = self.service.get_equipment_by_id(equipment_id)

        if equipment is None:
            return

        self.selected_equipment_id = equipment.id
        self.name_input.setText(equipment.name)
        self.category_input.setText(equipment.category)
        self.quantity_input.setText(str(equipment.quantity))

    def update_equipment(self) -> None:
        if self.selected_equipment_id is None:
            QMessageBox.warning(self, "No Equipment Selected", "Please select an equipment first.")
            return

        try:
            equipment = Equipment(self.name_input.text(), self.category_input.text(), self.quantity_input.text())
            equipment.id = self.selected_equipment_id
            self.service.update_equipment(equipment)

        except ValueError as error:
            QMessageBox.warning(self,"Invalid Equipment",str(error))
            return

        QMessageBox.information(self,"Updating Success",f"Equipment was updated successfully.")
        self.clear_inputs()
        self.refresh()

    def delete_equipment(self) -> None:
        if self.selected_equipment_id is None:
            QMessageBox.warning(self,"No Equipment Selected","Please select an equipment first.")
            return

        answer = QMessageBox.question(self,"Delete Equipment","Are you sure you want to delete this equipment?")
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.service.delete_equipment(self.selected_equipment_id)

        QMessageBox.information(self,"Deleting Success",f"Equipment was deleted successfully.")
        self.clear_inputs()
        self.refresh()

    def clear_inputs(self) -> None:
        self.name_input.clear()
        self.category_input.clear()
        self.quantity_input.clear()
        self.selected_equipment_id = None

    def refresh(self) -> None:
        equipments = self.service.get_equipment()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(equipments))

        for row, equipment in enumerate(equipments):
            values = [f"EQ-{equipment.id:03d}", equipment.name, equipment.category, equipment.quantity, equipment.available]

            for column, value in enumerate(values):
                item = SortableTableWidgetItem(str(value))
                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, equipment.id)
                elif column in (3, 4):
                    item.setData(Qt.ItemDataRole.UserRole, value)

                self.table.setItem(row, column, item)

        self.table.setSortingEnabled(True)
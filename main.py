import sys
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from database.database import Database
from features.borrowing_records.service import BorrowingRecordsService
from features.borrowing_records.view import BorrowingRecordsView
from features.dashboard.service import DashboardService
from features.dashboard.view import DashboardView
from features.equipment_borrowing.service import EquipmentBorrowingService
from features.equipment_borrowing.view import EquipmentBorrowingView
from features.equipment_management.service import EquipmentManagementService
from features.equipment_management.view import EquipmentManagementView
from features.equipment_return.service import EquipmentReturnService
from features.equipment_return.view import EquipmentReturnView
from features.search_equipment.service import EquipmentSearchService
from features.search_equipment.view import EquipmentSearchView


class BorrowBoxWindow(QWidget):
    def __init__(self, dashboard, equipment_management, equipment_borrowing, equipment_return, borrowing_records, search_equipment):
        super().__init__()
        self.setWindowTitle("BorrowBox")
        self.setWindowIcon(QIcon(str(Path(__file__).parent / "assets" / "logo" / "logo.svg")))
        self.resize(1200, 700)

        self.sidebar_expanded = True

        self.dashboard = dashboard
        self.equipment_management = equipment_management
        self.equipment_borrowing = equipment_borrowing
        self.equipment_return = equipment_return
        self.borrowing_records = borrowing_records
        self.search_equipment = search_equipment

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.build_sidebar()
        main_layout.addWidget(self.sidebar)

        content = QWidget()
        content.setObjectName("mainContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 18, 20, 20)
        content_layout.setSpacing(14)

        self.build_header()
        content_layout.addWidget(self.header)

        self.build_pages()
        content_layout.addWidget(self.pages)

        main_layout.addWidget(content)

    def build_sidebar(self) -> None:
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(225)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(14, 18, 14, 18)
        sidebar_layout.setSpacing(8)

        icons_path = Path(__file__).parent / "assets" / "icons"

        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(8)
        self.logo_label = QSvgWidget(str(Path(__file__).parent / "assets" / "logo" / "logo.svg"))
        self.logo_label.setObjectName("sidebarLogo")
        self.logo_label.setFixedSize(36, 36)

        self.wordmark_label = QSvgWidget(str(Path(__file__).parent / "assets" / "logo" / "wordmark.svg"))
        self.wordmark_label.setObjectName("sidebarWordmark")
        self.wordmark_label.setFixedHeight(25)

        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.wordmark_label)
        sidebar_layout.addLayout(logo_layout)
        sidebar_layout.addSpacing(20)

        self.dashboard_button = self.create_sidebar_button(str(icons_path / "dashboard.svg"), "Dashboard", 0)
        self.equipment_button = self.create_sidebar_button(str(icons_path / "equipment.svg"), "Equipment Management", 1)
        self.borrow_button = self.create_sidebar_button(str(icons_path / "borrow.svg"), "Equipment Borrowing", 2)
        self.return_button = self.create_sidebar_button(str(icons_path / "return.svg"), "Equipment Return", 3)
        self.records_button = self.create_sidebar_button(str(icons_path / "records.svg"), "Borrowing Records", 4)
        self.search_button = self.create_sidebar_button(str(icons_path / "search.svg"), "Search Equipment", 5)

        sidebar_layout.addWidget(self.dashboard_button)
        sidebar_layout.addWidget(self.equipment_button)
        sidebar_layout.addWidget(self.borrow_button)
        sidebar_layout.addWidget(self.return_button)
        sidebar_layout.addWidget(self.records_button)
        sidebar_layout.addWidget(self.search_button)
        sidebar_layout.addStretch()

        self.collapse_button = QPushButton("Collapse")
        self.collapse_button.setObjectName("collapseButton")
        self.collapse_button.setIcon(QIcon(str(Path(__file__).parent / "assets" / "icons" / "collapse.svg")))
        self.collapse_button.setIconSize(QSize(21, 21))
        self.collapse_button.setFixedHeight(40)
        self.collapse_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.collapse_button)

        self.dashboard_button.setChecked(True)

    def create_sidebar_button(self, icon_path: str, text: str, index: int) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("sidebarButton")
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(21, 21))
        button.setFixedHeight(44)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(True)
        button.clicked.connect(lambda: self.show_page(index))

        return button

    def build_header(self) -> None:
        self.header = QFrame()
        self.header.setObjectName("appHeader")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 6, 10, 6)

        self.header_title = QLabel("Dashboard")
        self.header_title.setObjectName("pageTitle")
        self.header_title.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.header_wordmark = QSvgWidget(str(Path(__file__).parent / "assets" / "logo" / "wordmark.svg"))
        self.header_wordmark.setObjectName("headerWordmark")
        self.header_wordmark.setFixedSize(161, 25)
        self.header_wordmark.hide()
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.header_wordmark)

    def build_pages(self) -> None:
        self.pages = QStackedWidget()
        self.dashboard_view = DashboardView(self.dashboard)
        self.equipment_management_view = EquipmentManagementView(self.equipment_management, self.refresh_all_pages)
        self.equipment_borrowing_view = EquipmentBorrowingView(self.equipment_borrowing, self.equipment_management, self.refresh_all_pages)
        self.equipment_return_view = EquipmentReturnView(self.equipment_return, self.refresh_all_pages)
        self.borrowing_records_view = BorrowingRecordsView(self.borrowing_records)
        self.search_equipment_view = EquipmentSearchView(self.search_equipment)

        self.pages.addWidget(self.dashboard_view)
        self.pages.addWidget(self.equipment_management_view)
        self.pages.addWidget(self.equipment_borrowing_view)
        self.pages.addWidget(self.equipment_return_view)
        self.pages.addWidget(self.borrowing_records_view)
        self.pages.addWidget(self.search_equipment_view)

    def show_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        self.refresh_current_page(index)

        buttons = [self.dashboard_button, self.equipment_button, self.borrow_button, self.return_button, self.records_button, self.search_button]

        for button in buttons:
            button.setChecked(False)

        buttons[index].setChecked(True)

        titles = ["Dashboard", "Equipment Management", "Equipment Borrowing", "Equipment Return", "Borrowing Records", "Search Equipment"]
        self.header_title.setText(titles[index])

    def toggle_sidebar(self) -> None:
        if self.sidebar_expanded:
            self.sidebar.setFixedWidth(72)
            self.wordmark_label.hide()

            self.dashboard_button.setText("")
            self.equipment_button.setText("")
            self.borrow_button.setText("")
            self.return_button.setText("")
            self.records_button.setText("")
            self.search_button.setText("")
            self.collapse_button.setText("")
            self.collapse_button.setIcon(QIcon(str(Path(__file__).parent / "assets" / "icons" / "expand.svg")))

            self.header_wordmark.show()
            self.sidebar_expanded = False

        else:
            self.sidebar.setFixedWidth(225)
            self.wordmark_label.show()

            self.dashboard_button.setText("Dashboard")
            self.equipment_button.setText("Equipment Management")
            self.borrow_button.setText("Borrow Equipment")
            self.return_button.setText("Return Equipment")
            self.records_button.setText("Borrowing Records")
            self.search_button.setText("Search Equipment")
            self.collapse_button.setText("Collapse")
            self.collapse_button.setIcon(QIcon(str(Path(__file__).parent / "assets" / "icons" / "collapse.svg")))

            self.header_wordmark.hide()
            self.sidebar_expanded = True

    def refresh_current_page(self, index: int) -> None:
        current_page = self.pages.widget(index)

        if hasattr(current_page, "refresh"):
            current_page.refresh()

        if hasattr(current_page, "search_equipment"):
            current_page.search_equipment()

    def refresh_all_pages(self) -> None:
        for index in range(self.pages.count()):
            page = self.pages.widget(index)

            if hasattr(page, "refresh"):
                page.refresh()

            if hasattr(page, "search_equipment"):
                page.search_equipment()


def main():
    database = Database()
    database.create_tables()

    app = QApplication(sys.argv)
    app.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())

    dashboard = DashboardService(database)
    equipment_management = EquipmentManagementService(database)
    equipment_borrowing = EquipmentBorrowingService(database)
    equipment_return = EquipmentReturnService(database)
    borrowing_records = BorrowingRecordsService(database)
    search_equipment = EquipmentSearchService(database)

    window = BorrowBoxWindow(dashboard, equipment_management, equipment_borrowing, equipment_return, borrowing_records, search_equipment)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
from pathlib import Path

from PyQt6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QPieSeries,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .service import DashboardService


class DashboardView(QWidget):
    def __init__(self, service: DashboardService):
        super().__init__()
        self.service = service
        self.setWindowTitle("Dashboard")
        self.build_ui()
        self.setStyleSheet((Path(__file__).with_name("style.qss")).read_text())
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(14)

        title = QLabel("BorrowBox Dashboard")
        title.setObjectName("dashboardTitle")
        layout.addWidget(title)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(12)
        self.total_equipment = self.create_card(cards_layout, "Total Equipment", 0, 0)
        self.total_quantity = self.create_card(cards_layout, "Total Quantity", 0, 1)
        self.available_equipment = self.create_card(cards_layout, "Available Equipment", 0, 2)
        self.borrowed_equipment = self.create_card(cards_layout, "Borrowed Equipment", 0, 3)
        self.total_borrowers = self.create_card(cards_layout, "Total Borrowers", 1, 0)
        self.active_borrowings = self.create_card(cards_layout, "Active Borrowings", 1, 1)
        self.returned_transactions = self.create_card(cards_layout, "Returned Transactions", 1, 2)
        self.total_transactions = self.create_card(cards_layout, "Total Transactions", 1, 3)
        layout.addLayout(cards_layout)

        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(12)
        self.availability_chart = QChartView()
        self.availability_chart.setObjectName("chartCard")
        self.category_chart = QChartView()
        self.category_chart.setObjectName("chartCard")
        charts_layout.addWidget(self.availability_chart)
        charts_layout.addWidget(self.category_chart)
        layout.addLayout(charts_layout)

        self.most_borrowed_chart = QChartView()
        self.most_borrowed_chart.setObjectName("chartCard")
        layout.addWidget(self.most_borrowed_chart)

    def create_card(self, layout: QGridLayout, title: str, row: int, column: int) -> QLabel:
        card = QWidget()
        card.setObjectName("statCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        value_label = QLabel("0")
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        layout.addWidget(card, row, column)

        return value_label

    def refresh(self) -> None:
        statistics = self.service.get_statistics()
        self.total_equipment.setText(str(statistics.total_equipment))
        self.total_quantity.setText(str(statistics.total_quantity))
        self.available_equipment.setText(str(statistics.available_equipment))
        self.borrowed_equipment.setText(str(statistics.borrowed_equipment))
        self.total_borrowers.setText(str(statistics.total_borrowers))
        self.active_borrowings.setText(str(statistics.active_borrowings))
        self.returned_transactions.setText(str(statistics.returned_transactions))
        self.total_transactions.setText(str(statistics.total_transactions))
        self.create_availability_chart(statistics)
        self.create_category_chart()
        self.create_most_borrowed_chart()

    def create_availability_chart(self, statistics) -> None:
        series = QPieSeries()
        available_slice = series.append("Available", statistics.available_equipment)
        borrowed_slice = series.append("Borrowed", statistics.borrowed_equipment)

        available_slice.setBrush(QColor("#4A5859"))
        borrowed_slice.setBrush(QColor("#C83E4D"))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Equipment Availability")
        chart.legend().setVisible(True)
        self.availability_chart.setChart(chart)

    def create_category_chart(self) -> None:
        records = self.service.get_borrowing_by_category()
        series = QBarSeries()
        bar_set = QBarSet("Borrowed Quantity")
        bar_set.setColor(QColor("#F4B860"))

        categories = []
        for category, quantity in records:
            categories.append(str(category))
            bar_set.append(quantity)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Borrowing by Category")

        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.addAxis(axis, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis)
        self.category_chart.setChart(chart)

    def create_most_borrowed_chart(self) -> None:
        records = self.service.get_most_borrowed_equipment()
        series = QBarSeries()
        bar_set = QBarSet("Borrowed Quantity")
        bar_set.setColor(QColor("#C83E4D"))

        categories = []
        for name, quantity in records:
            categories.append(str(name))
            bar_set.append(quantity)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Most Borrowed Equipment")
        chart.setTitleBrush(QColor("#32373B"))
        chart.setBackgroundBrush(QColor("#FFFFFF"))
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.addAxis(axis, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis)
        self.most_borrowed_chart.setChart(chart)
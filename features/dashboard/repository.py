from database.database import Database

from .model import Dashboard


class DashboardRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_statistics(self) -> Dashboard:
        with self.database.connect() as con:
            total_equipment = con.execute("SELECT COUNT(*) FROM equipments").fetchone()[0]
            total_quantity = con.execute("SELECT COALESCE(SUM(quantity), 0) FROM equipments").fetchone()[0]
            available_equipment = con.execute("SELECT COALESCE(SUM(available), 0) FROM equipments").fetchone()[0]
            total_borrowers = con.execute("SELECT COUNT(*) FROM borrowers").fetchone()[0]
            active_borrowings = con.execute("SELECT COUNT(*) FROM borrow_records WHERE status = 'Borrowed'").fetchone()[0]
            returned_transactions = con.execute("SELECT COUNT(*) FROM borrow_records WHERE status = 'Returned'").fetchone()[0]
            total_transactions = con.execute("SELECT COUNT(*) FROM borrow_records").fetchone()[0]

            borrowed_equipment = total_quantity - available_equipment

        return Dashboard(
            total_equipment=total_equipment,
            total_quantity=total_quantity,
            available_equipment=available_equipment,
            borrowed_equipment=borrowed_equipment,
            total_borrowers=total_borrowers,
            active_borrowings=active_borrowings,
            returned_transactions=returned_transactions,
            total_transactions=total_transactions
        )

    def get_borrowing_by_category(self) -> list[tuple]:
        with self.database.connect() as con:
            return con.execute(
                """
                SELECT e.category, SUM(br.quantity) FROM borrow_records br JOIN equipments e ON br.equipment_id = e.id
                GROUP BY e.category ORDER BY SUM(br.quantity) DESC
                """
            ).fetchall()

    def get_most_borrowed_equipment(self) -> list[tuple]:
        with self.database.connect() as con:
            return con.execute(
                """
                SELECT e.name, SUM(br.quantity) FROM borrow_records br JOIN equipments e ON br.equipment_id = e.id
                GROUP BY e.id, e.name ORDER BY SUM(br.quantity) DESC LIMIT 5
                """
            ).fetchall()
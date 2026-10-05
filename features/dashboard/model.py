from dataclasses import dataclass


@dataclass
class Dashboard:
    total_equipment: int
    total_quantity: int
    available_equipment: int
    borrowed_equipment: int
    total_borrowers: int
    active_borrowings: int
    returned_transactions: int
    total_transactions: int
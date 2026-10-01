from dataclasses import dataclass


@dataclass
class EquipmentReturn:
    transaction_id: int
    date_returned: str
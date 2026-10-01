from dataclasses import dataclass


@dataclass
class EquipmentSearchResult:
    id: int
    name: str
    category: str
    quantity: int
    available: int
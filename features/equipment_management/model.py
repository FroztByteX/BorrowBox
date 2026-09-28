from dataclasses import dataclass


@dataclass
class Equipment:
    name: str
    category: str
    quantity: int
    available: int | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.category = self.category.strip()

        if not self.name:
            raise ValueError("Name must not be empty")

        if not self.category:
            raise ValueError("Category must not be empty")

        try:
            self.quantity = int(self.quantity)
        except ValueError:
            raise ValueError("Quantity must be a number")

        if self.available is None:
            self.available = self.quantity

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if self.available < 0:
            raise ValueError("Available quantity must not be negative")
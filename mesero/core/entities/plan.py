from decimal import Decimal

class Plan:
    def __init__(self, name: str, description: str, price: Decimal, locations: int, tables: int, id: int = None):
        self.id = id  # Se asignará cuando se guarde en la DB
        self.name = name
        self.description = description
        self.locations = locations
        self.tables = tables
        self.price = Decimal(price)
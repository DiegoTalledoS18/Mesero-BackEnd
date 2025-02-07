from decimal import Decimal
from mesero.core.enums import PlanType

class Plan:
    def __init__(self, name: str, description: str, price: Decimal, locations: int, tables: int,  plan_type: PlanType, id: int = None):
        self.id = id  # Se asignará cuando se guarde en la DB
        self.name = name
        self.description = description
        self.locations = locations
        self.tables = tables
        self.price = Decimal(price)
        # Si recibimos un PlanType, usamos su valor, si es string lo usamos directamente
        if isinstance(plan_type, PlanType):
            self.plan_type = plan_type.value  # Esto dará "free" o "pay"
        else:
            self.plan_type = plan_type  # Ya es un string "free" o "pay"
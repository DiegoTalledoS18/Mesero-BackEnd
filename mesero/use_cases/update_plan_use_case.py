from mesero.repositories.plans_repository import PlanRepository
from mesero.core.entities.plan import Plan
from decimal import Decimal


class UpdatePlanUseCase:
    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    def execute(self, plan_id: int, name: str, description: str, locations: int, tables: int, price: Decimal) -> Plan:
        # Validaciones básicas
        if price < 0:
            raise ValueError("El precio debe ser mayor a 0.")

        # Verifica si locations es None antes de compararlo con un número
        if locations is not None and locations < 0:
            raise ValueError("La cantidad de locales no puede ser negativa.")

        if locations is not None and tables < 0:
            raise ValueError("La cantidad de mesas no puede ser negativa.")

        # Crear la entidad actualizada
        updated_plan = Plan(name, description, price, locations, tables, plan_id)

        # Llamar al repositorio para actualizar
        return self.plan_repository.update(updated_plan)

from mesero.repositories.plans_repository import PlanRepository
from mesero.core.entities.plan import Plan
from decimal import Decimal

class CreatePlanUseCase:
    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    def execute(self, name: str, description: str, locations: int, tables: int, price: Decimal) -> Plan:
        plan = Plan(name, description, price, locations, tables)
        return self.plan_repository.create(plan)

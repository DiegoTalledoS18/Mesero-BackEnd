from abc import ABC, abstractmethod
from mesero.core.entities.plan import Plan

class PlanRepository(ABC):
    @abstractmethod
    def create(self, plan: Plan) -> Plan:
        pass

    @abstractmethod
    def update(self, plan: Plan) -> Plan:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass
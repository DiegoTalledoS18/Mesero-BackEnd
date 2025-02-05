from mesero.repositories.plans_repository import PlanRepository

class DeletePlanUseCase:
    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    def execute(self, plan_id: int):
        return self.plan_repository.delete(plan_id)

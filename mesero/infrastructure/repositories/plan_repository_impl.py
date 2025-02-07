from mesero.repositories.plans_repository import PlanRepository
from mesero.core.entities.plan import Plan
from mesero.infrastructure.models.plan_model import PlanModel

class PlanRepositoryImpl(PlanRepository):
    def delete(self, id: int):
        try:
            # Buscar el plan en la base de datos
            plan_record = PlanModel.objects.get(id=id)

            # Eliminar el plan
            plan_record.delete()

        except PlanModel.DoesNotExist:
            # Si no se encuentra el plan, lanzar un error
            raise ValueError("El plan con el ID proporcionado no existe.")

    def update(self, plan: Plan) -> Plan:
        try:
            plan_record = PlanModel.objects.get(id=plan.id)
            plan_record.name = plan.name
            plan_record.description = plan.description
            plan_record.locations = plan.locations
            plan_record.tables = plan.tables
            plan_record.price = plan.price
            plan_record.plan_type = plan.plan_type
            plan_record.save()

            return Plan(plan_record.name, plan_record.description, plan_record.price, plan_record.locations, plan_record.tables, plan_record.plan_type, plan_record.id)
        except PlanModel.DoesNotExist:
            raise ValueError("El plan con el ID proporcionado no existe.")

    def create(self, plan: Plan) -> Plan:
        plan_model = PlanModel.objects.create(
            name=plan.name,
            description=plan.description,
            price=plan.price,
            locations=plan.locations,
            tables=plan.tables,
            plan_type=plan.plan_type,
        )
        return Plan(
            id=plan_model.id,
            name=plan_model.name,
            description=plan_model.description,
            price=plan_model.price,
            locations=plan_model.locations,
            tables=plan_model.tables,
            plan_type=plan_model.plan_type,
        )

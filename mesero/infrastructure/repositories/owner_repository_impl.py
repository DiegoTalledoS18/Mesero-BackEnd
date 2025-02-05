from mesero.repositories.owner_repository import OwnerRepository
from mesero.infrastructure.models.owner_model import OwnerModel
from mesero.core.entities.owner import Owner

class OwnerRepositoryImpl(OwnerRepository):
    def create(self, owner: Owner) -> Owner:
        owner_model = OwnerModel.objects.create(
            name=owner.name,
            email=owner.email,
            password=owner.password,
            phone=owner.phone,
            plan_id=owner.plan_id
        )
        return Owner(
            id=owner_model.id,
            name=owner_model.name,
            email=owner_model.email,
            password=owner_model.password,
            phone=owner_model.phone,
            plan_id=owner_model.plan_id
        )

from mesero.repositories.owner_repository import OwnerRepository
from mesero.infrastructure.models.owner_model import OwnerModel
from mesero.core.entities.owner import Owner
from typing import List

class OwnerRepositoryImpl(OwnerRepository):
    def delete(self, id: int):
        try:
            # Buscar el plan en la base de datos
            owner_record = OwnerModel.objects.get(id=id)

            # Eliminar el plan
            owner_record.delete()

        except OwnerModel.DoesNotExist:
            # Si no se encuentra el plan, lanzar un error
            raise ValueError("El owner con el ID proporcionado no existe.")

    def get_all(self) -> List[Owner]:
        owners = OwnerModel.objects.all()
        return [
            Owner(
                name=owner.name,
                email=owner.email,
                password=owner.password,
                phone=owner.phone,
                id=owner.id
            )
            for owner in owners
        ]

    def create(self, owner: Owner) -> Owner:
        owner_model = OwnerModel.objects.create(
            name=owner.name,
            email=owner.email,
            password=owner.password,
            phone=owner.phone
        )
        return Owner(
            id=owner_model.id,
            name=owner_model.name,
            email=owner_model.email,
            password=owner_model.password,
            phone=owner_model.phone
        )

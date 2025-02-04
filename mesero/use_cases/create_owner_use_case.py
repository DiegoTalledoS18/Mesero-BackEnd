from mesero.repositories.owner_repository import OwnerRepository
from mesero.core.entities.owner import Owner

class CreateOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, name: str, email: str, password: str, plan_id: int) -> Owner:
        # Aquí puedes encriptar la contraseña antes de guardarla
        new_owner = Owner(id=None, name=name, email=email, password=password, plan_id=plan_id)
        return self.owner_repository.create(new_owner)

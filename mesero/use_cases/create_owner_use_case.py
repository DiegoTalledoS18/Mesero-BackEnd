from mesero.repositories.owner_repository import OwnerRepository
from mesero.core.entities.owner import Owner
from django.contrib.auth.hashers import make_password


class CreateOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, name: str, email: str, password: str, phone: str) -> Owner:
        encrypted_password = make_password(password)  # Encriptar antes de guardar
        owner = Owner(name, email, encrypted_password, phone)
        return self.owner_repository.create(owner)

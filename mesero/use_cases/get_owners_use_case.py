from mesero.repositories.owner_repository import OwnerRepository

class GetOwnersUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self):
        return self.owner_repository.get_all()

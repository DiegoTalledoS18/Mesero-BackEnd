from mesero.repositories.owner_repository import OwnerRepository

class DeleteOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, owner_id: int):
        return self.owner_repository.delete(owner_id)

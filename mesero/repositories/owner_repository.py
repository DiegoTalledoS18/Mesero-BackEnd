from abc import ABC, abstractmethod
from mesero.core.entities.owner import Owner

class OwnerRepository(ABC):
    @abstractmethod
    def create(self, owner: Owner) -> Owner:
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

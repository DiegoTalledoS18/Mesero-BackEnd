from abc import ABC, abstractmethod
from mesero.core.entities.owner import Owner

class OwnerRepository(ABC):
    @abstractmethod
    def create(self, owner: Owner) -> Owner:
        pass

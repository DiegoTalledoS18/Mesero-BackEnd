from abc import ABC, abstractmethod
from mesero.core.entities.subscription import Subscription

class SubscriptionRepository(ABC):
    @abstractmethod
    def create(self, subscription: Subscription) -> Subscription:
        pass

    @abstractmethod
    def update(self, subscription: Subscription) -> Subscription:
        pass

    @abstractmethod
    def get_by_owner(self, owner_id):
        pass
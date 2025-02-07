from mesero.repositories.subscription_repository import SubscriptionRepository

class GetSubscriptionsUseCase:
    def __init__(self, subscription_repository: SubscriptionRepository):
        self.subscription_repository = subscription_repository

    def execute(self):
        return self.subscription_repository.get_all()

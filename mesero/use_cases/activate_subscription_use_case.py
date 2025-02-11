from mesero.repositories.subscription_repository import SubscriptionRepository
from mesero.core.entities.subscription import Subscription
from datetime import datetime, timedelta
from decimal import Decimal

class ActivateSubscriptionUseCase:
    def __init__(self, subscription_repository: SubscriptionRepository):
        self.subscription_repository = subscription_repository

    def execute(self, owner_id: int, plan_id: int, price_at_subscription: Decimal) -> Subscription:

        # Asignar fechas automáticamente
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)  # 1 mes después

        # Buscar suscripciones del owner_id
        existing_subscription = self.subscription_repository.get_by_owner(owner_id)

        if existing_subscription:
            if existing_subscription.is_active:
                # Caso 1: Ya existe una suscripción activa, no se hace nada
                return existing_subscription
            else:
                # Caso 2: Existe una suscripción inactiva, se reactiva con los nuevos datos
                existing_subscription.plan_id = plan_id
                existing_subscription.start_date = start_date
                existing_subscription.end_date = end_date
                existing_subscription.is_active = True
                # Solo actualizar price_at_subscription si se proporciona
                if price_at_subscription is not None:
                    existing_subscription.price_at_subscription = price_at_subscription

                return self.subscription_repository.update(existing_subscription)

        # Caso 3: No existe una suscripción, se crea una nueva
        new_subscription = Subscription(
            owner_id=owner_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            price_at_subscription=price_at_subscription
        )

        return self.subscription_repository.create(new_subscription)

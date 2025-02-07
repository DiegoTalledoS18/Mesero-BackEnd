from mesero.core.entities.subscription import Subscription
from mesero.infrastructure.models.subscription_model import SubscriptionModel
from mesero.repositories.subscription_repository import SubscriptionRepository
from typing import List

class SubscriptionRepositoryImpl(SubscriptionRepository):
    def get_all(self) -> List[Subscription]:
        subscriptions = SubscriptionModel.objects.all()
        return [
            Subscription(
                id=sub.id,
                owner_id=sub.owner_id,
                plan_id=sub.plan_id,
                start_date=sub.start_date,
                end_date=sub.end_date,
                is_active=sub.is_active,
                price_at_subscription=sub.price_at_subscription
            )
            for sub in subscriptions
        ]


    def get_by_owner(self, owner_id):
        try:
            subscription = SubscriptionModel.objects.filter(owner_id=owner_id).order_by('-start_date').first()
            if subscription:
                return Subscription(
                    id=subscription.id,
                    owner_id=subscription.owner_id,
                    plan_id=subscription.plan_id,
                    start_date=subscription.start_date,
                    end_date=subscription.end_date,
                    is_active=subscription.is_active,
                    price_at_subscription=subscription.price_at_subscription
                )
            return None
        except SubscriptionModel.DoesNotExist:
            return None

    def update(self, subscription: Subscription) -> Subscription:
        try:
            subscription_record = SubscriptionModel.objects.get(id=subscription.id)
            subscription_record.plan_id = subscription.plan_id
            subscription_record.start_date = subscription.start_date
            subscription_record.end_date = subscription.end_date
            subscription_record.is_active = subscription.is_active
            subscription_record.price_at_subscription = subscription.price_at_subscription
            subscription_record.save()

            return Subscription(subscription_record.owner_id, subscription_record.plan_id, subscription_record.start_date, subscription_record.end_date,
                        subscription_record.is_active, subscription_record.price_at_subscription, subscription_record.id)
        except SubscriptionModel.DoesNotExist:
            raise ValueError("Esta suscripcion con el ID proporcionado no existe.")

    def create(self, subscription: Subscription) -> Subscription:
        subscription_model = SubscriptionModel.objects.create(
            owner_id=subscription.owner_id,
            plan_id=subscription.plan_id,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            is_active=subscription.is_active,
            price_at_subscription=subscription.price_at_subscription,
        )
        return Subscription(
            id=subscription_model.id,
            owner_id=subscription_model.owner_id,
            plan_id=subscription_model.plan_id,
            start_date=subscription_model.start_date,
            end_date=subscription_model.end_date,
            is_active=subscription_model.is_active,
            price_at_subscription=subscription_model.price_at_subscription,
        )
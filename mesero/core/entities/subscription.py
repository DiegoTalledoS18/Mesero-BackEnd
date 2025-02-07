from decimal import Decimal
from datetime import datetime
from mesero.core.entities.plan import Plan

class Subscription:
    def __init__(self, owner_id: int, plan_id: int, start_date: datetime, end_date: datetime, is_active: bool, price_at_subscription: Decimal, id: int = None):
        self.id = id
        self.owner_id = owner_id
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.price_at_subscription = price_at_subscription

    def activate_subscription(self):
        self.is_active = True

    def deactivate_subscription(self):
        self.is_active = False

    def update_dates(self, new_start_date: datetime, new_end_date: datetime):
        self.start_date = new_start_date
        self.end_date = new_end_date

    def __str__(self):
        return f"Subscription {self.id} for User {self.owner_id} with Plan {self.plan_id}"

    def is_valid(self):
        # Verifica si la suscripción está activa y no ha expirado
        return self.is_active and self.end_date > datetime.now()

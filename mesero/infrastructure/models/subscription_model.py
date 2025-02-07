from django.db import models
from decimal import Decimal


class SubscriptionModel(models.Model):
    # Relación con el usuario que es el dueño de la suscripción
    owner = models.ForeignKey('OwnerModel', on_delete=models.CASCADE, related_name="subscriptions")

    # Relación con el plan de suscripción
    plan = models.ForeignKey('PlanModel', on_delete=models.CASCADE)

    # Fechas relevantes
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Estado de la suscripción
    is_active = models.BooleanField(default=True)

    # Precio en el momento de la suscripción
    price_at_subscription = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Subscription for {self.owner} - {self.plan}"

    class Meta:
        db_table = "subscriptions"
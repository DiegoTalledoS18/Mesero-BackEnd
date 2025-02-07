from django.db import models
from mesero.core.enums import PlanType

class PlanModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    locations = models.IntegerField(null=True, blank=True)  # None = Unlimited
    tables = models.IntegerField(null=True, blank=True)  # None = Unlimited
    plan_type = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.value) for tag in PlanType]  # Usa tag.value para que sea 'free' y 'pay'
    )


    class Meta:
        db_table = "plans"

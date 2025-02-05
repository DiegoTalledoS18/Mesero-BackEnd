from django.db import models

class PlanModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    locations = models.IntegerField(null=True, blank=True)  # None = Unlimited
    tables = models.IntegerField(null=True, blank=True)  # None = Unlimited


class Meta:
        db_table = "plans"

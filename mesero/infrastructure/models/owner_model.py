from django.db import models

class OwnerModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    plan_id = models.IntegerField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'owners'
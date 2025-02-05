from django.db import models

class OwnerModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    plan_id = models.IntegerField()

    class Meta:
        db_table = 'owners'

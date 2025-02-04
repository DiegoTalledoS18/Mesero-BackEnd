from django.db import models

class OwnerModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.TextField()  # Debe ser encriptada
    plan_id = models.IntegerField()

    class Meta:
        db_table = 'owners'

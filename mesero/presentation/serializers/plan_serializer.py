from rest_framework import serializers
from mesero.infrastructure.models.plan_model import PlanModel

class PlanSerializer(serializers.ModelSerializer):
    locations = serializers.IntegerField(required=False, allow_null=True)
    tables = serializers.IntegerField(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = PlanModel
        fields = ['name', 'description', 'locations', 'tables', 'price']

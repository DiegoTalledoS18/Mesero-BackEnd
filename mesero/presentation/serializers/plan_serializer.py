from rest_framework import serializers
from mesero.infrastructure.models.plan_model import PlanModel
from mesero.core.enums.plan_type import PlanType  # Importa el enum

class PlanSerializer(serializers.ModelSerializer):
    locations = serializers.IntegerField(required=False, allow_null=True)
    tables = serializers.IntegerField(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    plan_type = serializers.ChoiceField(choices=[(tag.name, tag.value) for tag in PlanType], default=PlanType.FREE.value)

    class Meta:
        model = PlanModel
        fields = ['name', 'description', 'locations', 'tables', 'price', 'plan_type']

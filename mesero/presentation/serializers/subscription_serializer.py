from rest_framework import serializers
from mesero.infrastructure.models.subscription_model import SubscriptionModel

class SubscriptionSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    start_date = serializers.DateTimeField(read_only=True)  # Solo lectura
    end_date = serializers.DateTimeField(read_only=True)  # Solo lectura
    is_active = serializers.BooleanField(read_only=True)  # Solo lectura
    price_at_subscription = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )  # Opcional

    class Meta:
        model = SubscriptionModel
        fields = [
            'owner_id',
            'plan_id',
            'start_date',
            'end_date',
            'is_active',
            'price_at_subscription'
        ]

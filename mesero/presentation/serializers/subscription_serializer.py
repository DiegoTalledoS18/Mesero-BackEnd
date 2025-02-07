from rest_framework import serializers
from mesero.infrastructure.models.subscription_model import SubscriptionModel

class SubscriptionSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()

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

from rest_framework import serializers

class StripeSubscriptionSerializer(serializers.Serializer):
    customer_email = serializers.EmailField()  # Corrige el typo y usa EmailField
    price_id = serializers.CharField()

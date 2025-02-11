import stripe
from django.conf import settings


class CreateSubscriptionUseCase:
    def execute(self, customer_email: str, price_id: str):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Crear cliente en Stripe
            customer = stripe.Customer.create(
                email=customer_email,
                description="Cliente para suscripción"
            )

            # Crear la suscripción
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"]
            )

            return subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Error: {e.user_message}")

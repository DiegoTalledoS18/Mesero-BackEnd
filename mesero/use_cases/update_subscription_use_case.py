import stripe
from django.conf import settings

class UpdateSubscriptionUseCase:
    def execute(self, subscription_id: str, new_price_id: str):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Obtener la suscripción actual
            subscription = stripe.Subscription.retrieve(subscription_id)

            # Actualizar la suscripción con el nuevo plan de precios
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                items=[{
                    "id": subscription["items"]["data"][0]["id"],  # ID del item de suscripción actual
                    "price": new_price_id,  # Nuevo plan de precios
                }],
                proration_behavior="none"
            )

            return {
                "status": "success",
                "subscription_id": updated_subscription.id,
                "new_price_id": new_price_id,
                "current_period_end": updated_subscription.current_period_end
            }

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Error: {e.user_message if hasattr(e, 'user_message') else str(e)}")

        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")

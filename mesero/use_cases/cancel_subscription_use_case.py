import stripe
from django.conf import settings

class CancelSubscriptionUseCase:
    def execute(self, subscription_id: str):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Buscar la suscripción en Stripe
            subscription = stripe.Subscription.retrieve(subscription_id)

            if subscription.status == "canceled":
                raise Exception("La suscripción ya está cancelada")

            # Cancelar la suscripción
            stripe.Subscription.delete(subscription_id)

            return {"status": "success", "message": "Suscripción cancelada correctamente"}

        except stripe.error.InvalidRequestError:
            raise Exception("La suscripción no existe o ya fue cancelada")

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Error: {e.user_message if hasattr(e, 'user_message') else str(e)}")

        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")

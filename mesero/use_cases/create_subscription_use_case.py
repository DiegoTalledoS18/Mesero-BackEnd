import stripe
from django.conf import settings


class CreateSubscriptionUseCase:
    def execute(self, customer_email: str, price_id: str, payment_method_id: str):
        try:
            if not settings.STRIPE_SECRET_KEY:
                raise Exception("Clave secreta de Stripe no configurada correctamente")
            else:
                stripe.api_key = settings.STRIPE_SECRET_KEY

            # Buscar si el cliente ya existe
            existing_customers = stripe.Customer.list(email=customer_email, limit=1)

            if existing_customers.data:
                customer = existing_customers.data[0]
            else:
                customer = stripe.Customer.create(
                    email=customer_email,
                    description="Cliente para suscripción"
                )

            # Verificar si el cliente ya tiene una suscripción activa
            existing_subscriptions = stripe.Subscription.list(
                customer=customer.id,
                status='active',
                limit=1
            )

            if existing_subscriptions.data:
                raise Exception("Ya existe una suscripción activa para este cliente")

            # Asociar método de pago
            stripe.PaymentMethod.attach(payment_method_id, customer=customer.id)

            # Configurar método de pago predeterminado
            stripe.Customer.modify(
                customer.id,
                invoice_settings={"default_payment_method": payment_method_id}
            )

            # Crear suscripción
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price_id}],
                default_payment_method=payment_method_id,
                expand=["latest_invoice.payment_intent"]
            )

            # Manejar el PaymentIntent
            if hasattr(subscription, 'latest_invoice') and \
                    hasattr(subscription.latest_invoice, 'payment_intent'):
                payment_intent = subscription.latest_invoice.payment_intent

                if payment_intent.status not in ['succeeded', 'requires_capture']:
                    payment_intent = stripe.PaymentIntent.confirm(payment_intent.id)

                    if payment_intent.status not in ['succeeded', 'requires_capture']:
                        raise stripe.error.StripeError(
                            message="El pago no pudo ser procesado"
                        )

            return subscription

        except stripe.error.StripeError as e:
            # Cancelar la suscripción si existe y hubo error en el pago
            if 'subscription' in locals():
                try:
                    stripe.Subscription.delete(subscription.id)
                except:
                    pass
            raise Exception(f"Stripe Error: {e.user_message if hasattr(e, 'user_message') else str(e)}")

        except Exception as e:
            # Cancelar la suscripción si existe y hubo error
            if 'subscription' in locals():
                try:
                    stripe.Subscription.delete(subscription.id)
                except:
                    pass
            raise Exception(f"Error inesperado: {str(e)}")
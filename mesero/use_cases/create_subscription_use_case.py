import stripe
from django.conf import settings


class CreateSubscriptionUseCase:
    def execute(self, customer_email: str, price_id: str, payment_method_id: str):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            print("Inicio del proceso de suscripción.")

            # 1️⃣ Crear cliente en Stripe (si no existe)
            print("Creando cliente en Stripe...")
            customer = stripe.Customer.create(
                email=customer_email,
                description="Cliente para suscripción"
            )
            print(f"Cliente creado: {customer.id}")

            # 2️⃣ Asociar el método de pago al cliente
            print("Asociando método de pago al cliente...")
            stripe.PaymentMethod.attach(payment_method_id, customer=customer.id)
            print(f"Método de pago {payment_method_id} asociado al cliente {customer.id}")

            # 3️⃣ Configurar el método de pago como predeterminado
            print("Configurando método de pago predeterminado...")
            stripe.Customer.modify(
                customer.id,
                invoice_settings={"default_payment_method": payment_method_id}
            )
            print("Método de pago predeterminado configurado.")

            # 4️⃣ Crear la suscripción y cobrar la primera cuota
            print("Creando suscripción...")
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price_id}],
                default_payment_method=payment_method_id,
                expand=["latest_invoice.payment_intent"]
            )
            print(f"Suscripción creada: {subscription.id}")

            # 5️⃣ Verificar si hay un PaymentIntent asociado antes de confirmar el pago
            if subscription.latest_invoice and subscription.latest_invoice.payment_intent:
                payment_intent_id = subscription.latest_invoice.payment_intent.id
                print(f"Confirmando PaymentIntent: {payment_intent_id}")

                payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
                print(f"Stripe PaymentIntent Response: {payment_intent}")

            else:
                print("No se encontró un PaymentIntent en la suscripción.")

            return subscription

        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
            raise Exception(f"Stripe Error: {e.user_message}")

        except Exception as e:
            print(f"Error inesperado: {e}")
            raise Exception(f"Error inesperado: {str(e)}")

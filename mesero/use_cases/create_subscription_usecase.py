from mesero.infrastructure.external_services.mercadopago_config import sdk
from datetime import datetime, timedelta


class CreateSubscriptionUseCase:
    def execute(self, customer_id: str, card_id: str, plan_id: int, price: float):
        try:
            # Primero necesitamos obtener un token de pago usando la tarjeta guardada
            card_payment_data = {
                "card_id": card_id,
                "security_code": "123",  # Para tarjetas de prueba
                "customer_id": customer_id
            }

            print("Datos para crear token de pago:", card_payment_data)
            card_token = sdk.card_token().create(card_payment_data)
            print("Respuesta de token de pago:", card_token)

            if "response" not in card_token:
                raise Exception(f"Error al crear token de pago: {card_token}")

            payment_token = card_token["response"]["id"]

            # Ahora creamos el pago con el token generado
            payment_data = {
                "transaction_amount": float(price),
                "token": payment_token,
                "description": f"Suscripción al plan {plan_id}",
                "installments": 1,
                "payment_method_id": "visa",  # O el método correspondiente
                "payer": {
                    "type": "customer",
                    "id": customer_id
                }
            }

            print("Datos del pago a crear:", payment_data)
            payment_response = sdk.payment().create(payment_data)
            print("Respuesta completa del pago:", payment_response)

            if "response" not in payment_response:
                error_msg = payment_response.get("message", "Error desconocido")
                raise Exception(f"Error en respuesta de pago: {error_msg}")

            return payment_response["response"]

        except Exception as e:
            print(f"Error detallado al procesar pago: {str(e)}")
            raise Exception(f"Error al procesar el pago: {str(e)}")
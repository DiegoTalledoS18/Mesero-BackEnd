from mesero.infrastructure.external_services.mercadopago_config import sdk
from datetime import datetime, timedelta

class CreateSubscriptionUseCase:
    def execute(self, customer_id: str, card_id: str, plan_id: int, price: float):
        payment_data = {
            "transaction_amount": price,
            "description": f"Suscripción al plan {plan_id}",
            "payment_method_id": "credit_card",
            "payer": {
                "type": "customer",
                "id": customer_id,
                "entity_type": "individual"
            },
            "installments": 1,
            "token": card_id
        }

        payment_response = sdk.payment().create(payment_data)

        if payment_response["status"] != 201:
            raise Exception("Error al procesar el pago")

        return payment_response["response"]

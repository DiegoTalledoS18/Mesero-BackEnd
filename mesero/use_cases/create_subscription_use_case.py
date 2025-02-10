from mesero.infrastructure.external_services.mercadopago_config import sdk
from datetime import datetime, timedelta


class CreateSubscriptionUseCase:
    def execute(self, payer_email: str, token: str, customer_id: str, card_id: str, plan_id: int, price: float):
        try:
            print("🟡 Creando suscripción preaprobada...")

            preapproval_data = {
                "payer_email": payer_email,  # REQUERIDO
                "card_token_id": token,  # REQUERIDO - Usando el token directamente
                "reason": f"Suscripción mensual - Plan {plan_id}",
                "external_reference": f"PLAN_{plan_id}_{customer_id}",
                "auto_recurring": {
                    "frequency": 1,  # REQUERIDO
                    "frequency_type": "months",  # REQUERIDO
                    "transaction_amount": float(price),
                    "currency_id": "PEN"  # REQUERIDO
                },
                "back_url": "https://tudominio.com/subscription/success",  # REQUERIDO
                "status": "authorized"  # Indica que ya tenemos método de pago
            }

            print("🟡 Datos de la suscripción:", preapproval_data)
            preapproval_response = sdk.preapproval().create(preapproval_data)
            print("🟢 Respuesta de suscripción:", preapproval_response)

            if "response" not in preapproval_response:
                error_msg = preapproval_response.get("message", "Error desconocido")
                raise Exception(f"❌ Error en respuesta de suscripción: {error_msg}")

            subscription_info = preapproval_response["response"]
            status = subscription_info.get("status")
            preapproval_id = subscription_info.get("id")

            print(f"🔍 Estado de la suscripción: {status} | ID: {preapproval_id}")

            if status == "authorized":
                print("✅ Suscripción creada y autorizada correctamente.")
            else:
                print(f"❌ Suscripción no autorizada. Estado: {status}")

            return {
                "status": status,
                "preapproval_id": preapproval_id,
                "subscription_info": subscription_info
            }

        except Exception as e:
            print(f"🚨 Error detallado al crear suscripción: {str(e)}")
            raise Exception(f"❌ Error al crear la suscripción: {str(e)}")
from mesero.infrastructure.external_services.mercadopago_config import sdk
from datetime import datetime, timedelta


class CreatePaymentUseCase:
    def execute(self, customer_id: str, card_id: str, plan_id: int, price: float):
        try:
            # Paso 1: Obtener un token de pago usando la tarjeta guardada
            card_payment_data = {
                "card_id": card_id,
                "security_code": "123",  # Solo para tarjetas de prueba
                "customer_id": customer_id
            }

            #print("🟡 Enviando datos para crear token de pago:", card_payment_data)
            card_token = sdk.card_token().create(card_payment_data)
            #print("🟢 Respuesta de token de pago:", card_token)

            if "response" not in card_token:
                raise Exception(f"❌ Error al crear token de pago: {card_token}")

            payment_token = card_token["response"].get("id")
            payment_method_id = card_token["response"].get("payment_method_id")

            if not payment_token:
                raise Exception("❌ No se generó un token de pago válido.")

            # Paso 2: Crear el pago con el token generado
            payment_data = {
                "transaction_amount": float(price),
                "token": payment_token,
                "description": f"Suscripción al plan {plan_id}",
                "installments": 1,
                "payment_method_id": payment_method_id,  # O el método correspondiente
                "payer": {
                    "type": "customer",
                    "id": customer_id
                }
            }

            ##print("🟡 Enviando datos del pago a MercadoPago:", payment_data)
            payment_response = sdk.payment().create(payment_data)
            ##print("🟢 Respuesta completa del pago:", payment_response)

            # Verificar si la respuesta tiene el campo "response"
            if "response" not in payment_response:
                error_msg = payment_response.get("message", "Error desconocido")
                raise Exception(f"❌ Error en respuesta de pago: {error_msg}")

            # Extraer estado del pago
            payment_info = payment_response["response"]
            status = payment_info.get("status")  # Estado general (approved, rejected, etc.)
            status_detail = payment_info.get("status_detail")  # Razón específica

            print(f"🔍 Estado del pago: {status} | Detalle: {status_detail}")

            if status == "approved":
                print("✅ Pago aprobado correctamente.")
            else:
                print(f"❌ Pago rechazado. Motivo: {status_detail}")

            return {
                "status": status,
                "status_detail": status_detail,
                "payment_response": payment_info
            }

        except Exception as e:
            print(f"🚨 Error detallado al procesar pago: {str(e)}")
            raise Exception(f"❌ Error al procesar el pago: {str(e)}")

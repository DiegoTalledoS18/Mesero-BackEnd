from mesero.use_cases.create_customer_use_case import CreateCustomerUseCase
from mesero.use_cases.save_card_use_case import SaveCardUseCase
from mesero.use_cases.create_subscription_use_case import CreateSubscriptionUseCase


class SubscriptionService:
    def __init__(self):
        self.create_customer_usecase = CreateCustomerUseCase()
        self.save_card_usecase = SaveCardUseCase()
        self.create_subscription_usecase = CreateSubscriptionUseCase()

    def subscribe_user(self, email: str, token: str, plan_id: int, price: float):
        try:
            ##print(f"Iniciando suscripción para {email}")

            # 1️⃣ Crear un cliente en Mercado Pago
            customer_id = self.create_customer_usecase.execute(email)
            #print(f"Cliente creado: {customer_id}")

            # 2️⃣ Guardar la tarjeta del cliente
            card_id = self.save_card_usecase.execute(customer_id, token)
            #print(f"Tarjeta guardada: {card_id}")

            # 3️⃣ Crear la suscripción con cobros mensuales automáticos
            payment_response = self.create_subscription_usecase.execute(email, token, customer_id, card_id, plan_id, price)
            print(f"Pago procesado: {payment_response}")

            return payment_response

        except Exception as e:
            print(f"Error en SubscriptionService: {str(e)}")
            raise e

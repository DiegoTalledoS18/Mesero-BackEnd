from mesero.use_cases.create_customer_use_case import CreateCustomerUseCase
from mesero.use_cases.save_card_use_case import SaveCardUseCase
from mesero.use_cases.create_subscription_usecase import CreateSubscriptionUseCase

class SubscriptionService:
    def __init__(self):
        self.create_customer_usecase = CreateCustomerUseCase()
        self.save_card_usecase = SaveCardUseCase()
        self.create_subscription_usecase = CreateSubscriptionUseCase()

    def subscribe_user(self, email: str, token: str, plan_id: int, price: float):
        # 1️⃣ Crear un cliente en Mercado Pago
        customer_id = self.create_customer_usecase.execute(email)

        # 2️⃣ Guardar la tarjeta del cliente
        card_id = self.save_card_usecase.execute(customer_id, token)

        # 3️⃣ Crear la suscripción con cobros mensuales automáticos
        payment_response = self.create_subscription_usecase.execute(customer_id, card_id, plan_id, price)

        return payment_response

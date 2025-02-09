from mesero.infrastructure.external_services.mercadopago_config import sdk

class CreateCustomerUseCase:
    def execute(self, email: str):
        customer_data = {"email": email}
        customer_response = sdk.customer().create(customer_data)

        if customer_response["status"] != 201:
            raise Exception("Error al crear el cliente en Mercado Pago")

        return customer_response["response"]["id"]  # customer_id

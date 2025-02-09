from mesero.infrastructure.external_services.mercadopago_config import sdk

class SaveCardUseCase:
    def execute(self, customer_id: str, token: str):
        card_data = {"token": token}
        card_response = sdk.card().create(customer_id, card_data)

        if card_response["status"] != 201:
            raise Exception("Error al guardar la tarjeta")

        return card_response["response"]["id"]  # card_id

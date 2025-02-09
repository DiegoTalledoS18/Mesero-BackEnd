from mesero.infrastructure.external_services.mercadopago_config import sdk


class SaveCardUseCase:
    def execute(self, customer_id: str, token: str):
        try:
            # Primero verificar si la tarjeta ya existe
            cards_response = sdk.card().list_all(customer_id)
            #print("Tarjetas existentes:", cards_response)

            # Intentar guardar la nueva tarjeta
            card_data = {
                "token": token,
                "customer_id": customer_id
            }
            #print(f"Guardando tarjeta para cliente {customer_id}")
            card_response = sdk.card().create(customer_id, card_data)

            print("Respuesta de creación de tarjeta:", card_response)

            if "error" in card_response:
                error_msg = card_response.get("message", "Error desconocido")
                raise Exception(f"MP Error: {error_msg}")

            if "response" not in card_response:
                raise Exception("Respuesta inválida de Mercado Pago")

            return card_response["response"]["id"]

        except Exception as e:
            print(f"Error detallado al guardar tarjeta: {str(e)}")
            raise Exception(f"Error al guardar la tarjeta: {str(e)}")

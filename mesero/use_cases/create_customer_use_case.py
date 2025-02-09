from mesero.infrastructure.external_services.mercadopago_config import sdk


class CreateCustomerUseCase:
    def execute(self, email: str):
        try:
            # Primero buscar si el cliente existe
            search_response = sdk.customer().search({"email": email})
            ##print("Búsqueda de cliente:", search_response)

            if "response" in search_response and search_response["response"].get("results"):
                # Cliente existe, retornar el ID existente
                customer_id = search_response["response"]["results"][0]["id"]
               # print(f"Cliente existente encontrado: {customer_id}")
                return customer_id

            # Si no existe, crear nuevo cliente
            customer_data = {
                "email": email,
                "description": "Cliente de prueba"
            }
            #print("Creando nuevo cliente:", customer_data)
            customer_response = sdk.customer().create(customer_data)

            #print("Respuesta de creación:", customer_response)

            if "error" in customer_response:
                error_msg = customer_response.get("message", "Error desconocido")
                raise Exception(f"MP Error: {error_msg}")

            if "response" not in customer_response:
                raise Exception("Respuesta inválida de Mercado Pago")

            return customer_response["response"]["id"]

        except Exception as e:
            print(f"Error detallado al crear/buscar cliente: {str(e)}")
            raise Exception(f"Error con el cliente en Mercado Pago: {str(e)}")

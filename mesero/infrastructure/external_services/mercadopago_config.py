from django.conf import settings
import mercadopago
import os

ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")

if not ACCESS_TOKEN:
    raise ValueError("MERCADOPAGO_ACCESS_TOKEN no está definido en las variables de entorno.")

sdk = mercadopago.SDK(ACCESS_TOKEN)

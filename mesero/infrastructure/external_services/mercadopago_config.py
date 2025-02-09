from django.conf import settings
import mercadopago
import os

ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")
PUBLIC_KEY = os.getenv("MERCADOPAGO_PUBLIC_KEY", "")

if not ACCESS_TOKEN:
    raise ValueError("MERCADOPAGO_ACCESS_TOKEN no está definido en las variables de entorno.")
if not PUBLIC_KEY:
    raise ValueError("MERCADOPAGO_PUBLIC_KEY no está definido en las variables de entorno.")

sdk = mercadopago.SDK(ACCESS_TOKEN)
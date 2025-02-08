import mercadopago
from django.conf import settings

# Configurar el SDK con tu Access Token
mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

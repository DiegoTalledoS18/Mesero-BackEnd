from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from mesero.infrastructure.repositories.subscription_repository_impl import SubscriptionRepositoryImpl
from mesero.presentation.serializers.subscription_serializer import SubscriptionModel, SubscriptionSerializer
from mesero.use_cases.activate_subscription_use_case import ActivateSubscriptionUseCase
from mesero.use_cases.get_subscriptions_use_case import GetSubscriptionsUseCase
from mesero.infrastructure.services.subscription_service import SubscriptionService

class SubscriptionView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subscription_service = SubscriptionService()

    def post(self, request):
        try:
            print("Request data:", request.data)  # Ver los datos completos que llegan

            email = request.data.get("email")
            token = request.data.get("token")
            plan_id = request.data.get("plan_id")
            price = request.data.get("price")

            print("Valores extraídos:")
            print(f"email: {email}")
            print(f"token: {token}")
            print(f"plan_id: {plan_id}")
            print(f"price: {price}")
            print(f"tipo de price: {type(price)}")

            if not email or not token or not plan_id or not price:
                missing_fields = []
                if not email: missing_fields.append("email")
                if not token: missing_fields.append("token")
                if not plan_id: missing_fields.append("plan_id")
                if not price: missing_fields.append("price")
                return Response(
                    {"error": f"Campos faltantes: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                price = float(price)
            except ValueError:
                return Response(
                    {"error": f"El precio debe ser un número válido. Recibido: {price}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            print("Llamando a subscribe_user con:")
            print(f"email: {email}, token: {token}, plan_id: {plan_id}, price: {price}")

            payment_response = self.subscription_service.subscribe_user(email, token, plan_id, price)

            print("Respuesta del servicio:", payment_response)
            return Response(payment_response, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error específico:", str(e))  # Log del error específico
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionCreateView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = SubscriptionModel.objects.all()

    def perform_create(self, serializer):
        # Instanciar repositorio y caso de uso
        plan_repository = SubscriptionRepositoryImpl()
        create_subscription_use_case = ActivateSubscriptionUseCase(plan_repository)

        # Obtener datos validados
        data = serializer.validated_data
        print("DATA RECIBIDA:", data)

        plan = create_subscription_use_case.execute(
            owner_id=data['owner_id'],
            plan_id=data['plan_id'],
            price_at_subscription=data['price_at_subscription'],
            payer_email="emailpaga@gmail.com"
        )

        # Guardar y devolver la instancia creada
        serializer.instance = plan

class SubscriptionListView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = SubscriptionModel.objects.all()

    def get_queryset(self):
        # Instanciar repositorio y caso de uso
        subscription_repository = SubscriptionRepositoryImpl()
        get_all_subscriptions_use_case = GetSubscriptionsUseCase(subscription_repository)

        # Ejecutar el caso de uso y devolver los datos
        return get_all_subscriptions_use_case.execute()
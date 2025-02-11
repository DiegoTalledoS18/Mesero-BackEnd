from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.generics import ListAPIView
from mesero.infrastructure.repositories.subscription_repository_impl import SubscriptionRepositoryImpl
from mesero.presentation.serializers.subscription_serializer import SubscriptionModel, SubscriptionSerializer
from mesero.presentation.serializers.stripe_subscription_serializer import StripeSubscriptionSerializer
from mesero.use_cases.activate_subscription_use_case import ActivateSubscriptionUseCase
from mesero.use_cases.create_subscription_use_case import CreateSubscriptionUseCase
from mesero.use_cases.get_subscriptions_use_case import GetSubscriptionsUseCase
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
import stripe


class SubscriptionCreateView(CreateAPIView):
    serializer_class = StripeSubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_email = serializer.validated_data["customer_email"]
        price_id = serializer.validated_data["price_id"]
        payment_method_id = serializer.validated_data["payment_method_id"]

        use_case = CreateSubscriptionUseCase()

        try:
            subscription = use_case.execute(customer_email, price_id, payment_method_id)
            return Response({
                "status": "success",
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_message = str(e)

            if "Ya existe una suscripción activa" in error_message:
                return Response({
                    "status": "error",
                    "message": "Ya existe una suscripción activa para este cliente"
                }, status=status.HTTP_409_CONFLICT)

            elif "Stripe Error" in error_message:
                return Response({
                    "status": "error",
                    "message": "Error procesando el pago",
                    "detail": error_message
                }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({
                    "status": "error",
                    "message": "Error interno del servidor",
                    "detail": error_message
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubscriptionActivateView(CreateAPIView):
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
            price_at_subscription=data['price_at_subscription']
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
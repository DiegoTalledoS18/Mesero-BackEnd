from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.generics import ListAPIView
from mesero.infrastructure.repositories.subscription_repository_impl import SubscriptionRepositoryImpl
from mesero.presentation.serializers.subscription_serializer import SubscriptionModel, SubscriptionSerializer
from mesero.presentation.serializers.stripe_subscription_serializer import StripeSubscriptionSerializer
from mesero.use_cases.activate_subscription_use_case import ActivateSubscriptionUseCase
from mesero.use_cases.create_subscription_use_case import CreateSubscriptionUseCase
from mesero.use_cases.get_subscriptions_use_case import GetSubscriptionsUseCase
from django.http import JsonResponse
import stripe

class SubscriptionCreateView(CreateAPIView):
    serializer_class = StripeSubscriptionSerializer  # Agrega el serializador

    def perform_create(self, serializer):
        data = serializer.validated_data
        print("DATA RECIBIDA:", data)
        customer_email = serializer.validated_data["customer_email"]
        price_id = serializer.validated_data["price_id"]
        payment_method_id = serializer.validated_data["payment_method_id"]

        use_case = CreateSubscriptionUseCase()

        try:
            subscription = use_case.execute(customer_email, price_id, payment_method_id)
            return JsonResponse({
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

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
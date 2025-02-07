from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.generics import ListAPIView
from mesero.infrastructure.repositories.subscription_repository_impl import SubscriptionRepositoryImpl
from mesero.presentation.serializers.subscription_serializer import SubscriptionModel, SubscriptionSerializer
from mesero.use_cases.create_subscription_use_case import CreateSubscriptionUseCase
from mesero.use_cases.get_subscriptions_use_case import GetSubscriptionsUseCase


class SubscriptionCreateView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = SubscriptionModel.objects.all()

    def perform_create(self, serializer):
        # Instanciar repositorio y caso de uso
        plan_repository = SubscriptionRepositoryImpl()
        create_subscription_use_case = CreateSubscriptionUseCase(plan_repository)

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
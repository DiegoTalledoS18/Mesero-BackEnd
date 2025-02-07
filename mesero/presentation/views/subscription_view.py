from rest_framework.generics import CreateAPIView, UpdateAPIView

from mesero.infrastructure.repositories.subscription_repository_impl import SubscriptionRepositoryImpl
from mesero.presentation.serializers.subscription_serializer import SubscriptionModel, SubscriptionSerializer
from mesero.use_cases.create_subscription_use_case import CreateSubscriptionUseCase


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
            start_date=data['start_date'],
            end_date=data['end_date'],
            price_at_subscription=data['price_at_subscription']
        )

        # Guardar y devolver la instancia creada
        serializer.instance = plan
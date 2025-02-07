# mesero/presentation/views/plan_view.py

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mesero.presentation.serializers.plan_serializer import PlanSerializer
from mesero.use_cases.update_plan_use_case import UpdatePlanUseCase
from mesero.use_cases.create_plan_use_case import CreatePlanUseCase
from mesero.use_cases.delete_plan_use_case import DeletePlanUseCase
from mesero.infrastructure.repositories.plan_repository_impl import PlanRepositoryImpl
from mesero.infrastructure.models.plan_model import PlanModel
from mesero.core.enums import PlanType
from decimal import Decimal

# Vista para crear un plan
class PlanCreateView(CreateAPIView):
    serializer_class = PlanSerializer
    queryset = PlanModel.objects.all()

    def perform_create(self, serializer):
        # Instanciar repositorio y caso de uso
        plan_repository = PlanRepositoryImpl()
        create_plan_use_case = CreatePlanUseCase(plan_repository)

        # Obtener datos validados
        data = serializer.validated_data
        print("DATA RECIBIDA:", data)  # <-- Para verificar qué datos llegan
        plan_type = PlanType[data.get('plan_type', 'FREE')]

        plan = create_plan_use_case.execute(
            name=data['name'],
            description=data['description'],
            locations=data.get('locations'),
            tables=data.get('tables'),
            price=data['price'],
            plan_type=plan_type
        )

        # Guardar y devolver la instancia creada
        serializer.instance = plan


# Vista para actualizar un plan
class PlanUpdateView(UpdateAPIView):
    queryset = PlanModel.objects.all()
    serializer_class = PlanSerializer

    def update(self, request, *args, **kwargs):
        # Obtener el ID del plan desde los parámetros de la URL
        plan_id = self.kwargs.get("pk")

        # Obtener los datos del cuerpo de la solicitud
        data = request.data

        # Obtener el plan existente
        plan = self.get_object()  # Usa `get_object()` para obtener el plan basado en el ID

        # Comprobar si los campos están presentes en la solicitud, si no, mantener el valor actual
        name = data.get("name")
        description = data.get("description")

        # Si no hay "name", mantener el nombre actual
        if not name:
            name = plan.name

        # Si no hay "description", mantener la descripción actual
        if not description:
            description = plan.description

        # Validar y asignar 'locations'
        locations_str = data.get("locations", str(plan.locations))  # Si no hay "locations", usa la cantidad actual
        try:
            locations = int(locations_str) if locations_str else plan.locations  # Si "quantity" es vacío, usa el valor actual
        except ValueError:
            locations = plan.locations  # Si no se puede convertir, mantén el valor actual

        # Validar y asignar 'tables'
        tables_str = data.get("tables", str(plan.tables))  # Si no hay "quantity", usa la cantidad actual
        try:
            tables = int(tables_str) if tables_str else plan.tables  # Si "quantity" es vacío, usa el valor actual
        except ValueError:
            tables = plan.tables  # Si no se puede convertir, mantén el valor actual

        # Validar y asignar 'price'
        price_str = data.get("price", str(plan.price))  # Si no hay "price", usa el precio actual
        try:
            price = Decimal(price_str) if price_str else plan.price  # Si "price" es vacío, usa el valor actual
        except ValueError:
            price = plan.price  # Si no se puede convertir, mantén el valor actual

        # Validar y asignar 'plan_type'
        plan_type_str = data.get("plan_type", plan.plan_type)  # Si no hay "plan_type", usa el tipo actual
        try:
            plan_type = PlanType[plan_type_str.upper()]  # Convertir la cadena a PlanType (asegurándonos de que sea mayúscula)
        except KeyError:
            plan_type = plan.plan_type  # Si no es un valor válido, mantener el tipo actual


        # Instanciar el caso de uso y actualizar el plan
        plan_repository = PlanRepositoryImpl()
        use_case = UpdatePlanUseCase(plan_repository)

        try:
            updated_plan = use_case.execute(plan_id, name, description, locations, tables, price, plan_type)
            return Response(PlanSerializer(updated_plan).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PlanDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        # Obtener el ID del plan desde la URL
        plan_id = self.kwargs.get("pk")

        if not plan_id:
            return Response({"error": "Plan ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Instanciar el repositorio y el caso de uso
        plan_repository = PlanRepositoryImpl()
        delete_plan_use_case = DeletePlanUseCase(plan_repository)

        try:
            # Ejecutar el caso de uso para eliminar el plan
            delete_plan_use_case.execute(plan_id)

            return Response({"message": "Plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
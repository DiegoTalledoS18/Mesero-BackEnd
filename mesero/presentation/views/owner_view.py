# mesero/presentation/views/owner_view.py

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mesero.core.entities.owner import Owner
from mesero.presentation.serializers.owner_serializer import OwnerSerializer
from mesero.infrastructure.models.owner_model import OwnerModel
from mesero.infrastructure.repositories.owner_repository_impl import OwnerRepositoryImpl
from mesero.use_cases.get_owners_use_case import GetOwnersUseCase
from mesero.use_cases.delete_owner_use_case import DeleteOwnerUseCase

class OwnerCreateView(CreateAPIView):
    serializer_class = OwnerSerializer

class OwnerListView(ListAPIView):
    serializer_class = OwnerSerializer
    queryset = OwnerModel.objects.all()

    def get_queryset(self):
        # Instanciar repositorio y caso de uso
        owner_repository = OwnerRepositoryImpl()
        get_all_owners_use_case = GetOwnersUseCase(owner_repository)

        # Ejecutar el caso de uso y devolver los datos
        return get_all_owners_use_case.execute()

class OwnerDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        # Obtener el ID del plan desde la URL
        owner_id = self.kwargs.get("pk")

        if not owner_id:
            return Owner({"error": "Owner ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Instanciar el repositorio y el caso de uso
        plan_repository = OwnerRepositoryImpl()
        delete_plan_use_case = DeleteOwnerUseCase(plan_repository)

        try:
            # Ejecutar el caso de uso para eliminar el plan
            delete_plan_use_case.execute(owner_id)

            return Response({"message": "Owner deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mesero.use_cases.create_owner_use_case import CreateOwnerUseCase
from mesero.infrastructure.repositories.owner_repository_impl import OwnerRepositoryImpl

class OwnerCreateView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")  # Recuerda encriptarla en el use case
        plan_id = data.get("plan_id")

        # Inyección de dependencias manual
        owner_repository = OwnerRepositoryImpl()
        create_owner_use_case = CreateOwnerUseCase(owner_repository)

        new_owner = create_owner_use_case.execute(name, email, password, plan_id)

        return Response(
            {
                "id": new_owner.id,
                "name": new_owner.name,
                "email": new_owner.email,
                "plan_id": new_owner.plan_id,
            },
            status=status.HTTP_201_CREATED
        )

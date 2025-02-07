# mesero/presentation/serializers/owner_serializer.py
from rest_framework import serializers
from mesero.infrastructure.repositories.owner_repository_impl import OwnerRepositoryImpl
from mesero.use_cases.create_owner_use_case import CreateOwnerUseCase



class OwnerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(max_length=20)
    id = serializers.IntegerField(read_only=True)  # Solo lectura

    def create(self, validated_data):
        repository = OwnerRepositoryImpl()
        use_case = CreateOwnerUseCase(repository)
        return use_case.execute(**validated_data)

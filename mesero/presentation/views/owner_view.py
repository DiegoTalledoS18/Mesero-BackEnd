# mesero/presentation/views/owner_view.py

from rest_framework.generics import CreateAPIView
from mesero.presentation.serializers.owner_serializer import OwnerSerializer

class OwnerCreateView(CreateAPIView):
    serializer_class = OwnerSerializer
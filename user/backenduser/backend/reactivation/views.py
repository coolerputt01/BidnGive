from rest_framework import generics, permissions
from .models import ReactivationRequest
from .serializers import ReactivationRequestSerializer

class RequestReactivationView(generics.CreateAPIView):
    serializer_class = ReactivationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import ReactivationRequest
from accounts.models import User

class ListDisabledUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(is_disabled=True)
        return Response([{"id": u.id, "username": u.username, "email": u.email} for u in users])

class ApproveReactivationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_disabled=True)
            user.is_disabled = False
            user.save()
            ReactivationRequest.objects.filter(user=user).update(approved=True)
            return Response({"message": "User reactivated."})
        except User.DoesNotExist:
            return Response({"error": "User not found or not disabled."}, status=404)
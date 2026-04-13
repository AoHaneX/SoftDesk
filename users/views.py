from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .permission import IsSelf

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        # An authenticated user can only see themselves
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        # Account creation allowed without authentication
        if self.action == "create":
            return [AllowAny()]

        # All other actions require authentication
        if self.action in ["list", "retrieve", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSelf()]

        return [IsAuthenticated()]

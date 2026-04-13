from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelf(BasePermission):
    """
    Autorise uniquement l'accès à son propre profil utilisateur.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj
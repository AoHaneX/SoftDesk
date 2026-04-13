from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributor


class IsProjectContributor(BasePermission):
    """
    Allows access only to project contributors.
    """

    def has_object_permission(self, request, view, obj):
        # Handle Project case
        project = getattr(obj, "project", obj)

        return Contributor.objects.filter(user=request.user, project=project).exists()


class IsAuthorOrReadOnly(BasePermission):
    """
    The author can modify/delete.
    Other authorized users can only read.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return getattr(obj, "author_user", None) == request.user


class IsProjectAuthor(BasePermission):
    """
    Only the project author can manage contributors.
    """

    def has_object_permission(self, request, view, obj):
        project = getattr(obj, "project", None)
        if project is None:
            return False
        return project.author_user == request.user

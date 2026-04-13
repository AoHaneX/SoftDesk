from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .permission import IsProjectContributor, IsAuthorOrReadOnly, IsProjectAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Project.objects.filter(contributors__user=self.request.user)
            .select_related("author_user")
            .distinct()
            .order_by("id")
        )

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)

        Contributor.objects.get_or_create(
            user=self.request.user,
            project=project,
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]

        return [IsAuthenticated()]


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Contributor.objects.filter(project__contributors__user=self.request.user)
            .select_related("user", "project")
            .distinct()
            .order_by("id")
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsProjectContributor()]

        if self.action in ["create", "destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsProjectAuthor()]

        return [IsAuthenticated()]


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Issue.objects.filter(project__contributors__user=self.request.user)
            .select_related("project", "author_user", "assignee_user")
            .distinct()
            .order_by("id")
        )

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]

        return [IsAuthenticated()]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Comment.objects.filter(issue__project__contributors__user=self.request.user)
            .select_related("issue", "author_user", "issue__project")
            .distinct()
            .order_by("created_time")
        )

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]

        return [IsAuthenticated()]
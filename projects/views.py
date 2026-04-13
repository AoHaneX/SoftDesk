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
        # A user can only see projects they contribute to
        return (
            Project.objects.filter(contributors__user=self.request.user)
            .select_related(
                "author_user"
            )  # Optimizes query by fetching author in same SQL query
            .distinct()
            .order_by("id")
        )

    def perform_create(self, serializer):
        # The authenticated user becomes the author of the project
        project = serializer.save(author_user=self.request.user)

        # The author is automatically added as a contributor
        Contributor.objects.get_or_create(
            user=self.request.user,
            project=project,
        )

    def get_permissions(self):
        # Read and create actions require authentication only
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]

        # Update and delete actions are restricted to the project author
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]

        return [IsAuthenticated()]


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # A user can only see contributors of projects they are part of
        return (
            Contributor.objects.filter(project__contributors__user=self.request.user)
            .select_related(
                "user", "project"
            )  # Avoids extra queries for related objects
            .distinct()
            .order_by("id")
        )

    def get_permissions(self):
        # Contributors can be viewed by project members
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsProjectContributor()]

        # Only the project author can manage contributors
        if self.action in ["create", "destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsProjectAuthor()]

        return [IsAuthenticated()]


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # A user can only see issues from projects they contribute to
        return (
            Issue.objects.filter(project__contributors__user=self.request.user)
            .select_related(
                "project", "author_user", "assignee_user"
            )  # Optimizes related data fetching
            .distinct()
            .order_by("id")
        )

    def perform_create(self, serializer):
        # The authenticated user becomes the author of the issue
        serializer.save(author_user=self.request.user)

    def get_permissions(self):
        # Contributors can read and create issues
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]

        # Only the issue author can update or delete it
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]

        return [IsAuthenticated()]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # A user can only see comments from issues in projects they contribute to
        return (
            Comment.objects.filter(issue__project__contributors__user=self.request.user)
            .select_related(
                "issue", "author_user", "issue__project"
            )  # Reduces SQL queries for nested relations
            .distinct()
            .order_by("created_time")
        )

    def perform_create(self, serializer):
        # The authenticated user becomes the author of the comment
        serializer.save(author_user=self.request.user)

    def get_permissions(self):
        # Contributors can read and create comments
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]

        # Only the comment author can update or delete it
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]

        return [IsAuthenticated()]

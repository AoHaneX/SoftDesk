from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("id")
    serializer_class = ProjectSerializer
    # permission_classes = [AllowAny]


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by("id")
    serializer_class = ContributorSerializer


# permission_classes = [AllowAny]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by("id")
    serializer_class = IssueSerializer


# permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("created_time")
    serializer_class = CommentSerializer
    # permission_classes = [AllowAny]

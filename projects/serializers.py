from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


# TRransforme les instances de Project et Contributor en JSON et inversement, pour les API REST.
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author_user",
            "created_time",
        ]
        read_only_fields = ["id", "author_user", "created_time"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "project",
            "author_user",
            "assignee_user",
            "created_time",
        ]
        read_only_fields = ["id", "author_user", "created_time"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "description",
            "author_user",
            "issue",
            "created_time",
        ]
        read_only_fields = ["id", "author_user", "created_time"]

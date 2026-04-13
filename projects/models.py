from django.conf import settings
from django.db import models
import uuid


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = "BACK_END", "Back-end"
        FRONT_END = "FRONT_END", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    title = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ProjectType.choices)
    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"


class Issue(models.Model):
    class TagChoices(models.TextChoices):
        BUG = "BUG", "Bug"
        FEATURE = "FEATURE", "Feature"
        TASK = "TASK", "Task"

    class PriorityChoices(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class StatusChoices(models.TextChoices):
        TO_DO = "TO_DO", "To do"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        FINISHED = "FINISHED", "Finished"

    title = models.CharField(max_length=128)
    description = models.TextField()
    tag = models.CharField(max_length=20, choices=TagChoices.choices)
    priority = models.CharField(max_length=20, choices=PriorityChoices.choices)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.TO_DO,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues",
    )
    assignee_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    author_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id}"

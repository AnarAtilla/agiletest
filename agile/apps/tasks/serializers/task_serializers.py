from datetime import datetime
from typing import Any, List

from django.utils import timezone
from rest_framework import serializers

from apps.projects.models import Project
from apps.projects.serializers.project_serializers import ProjectShortInfoSerializer
from apps.tasks.choices.priorities import Priority
from apps.tasks.models import Tag, Task
from apps.tasks.serializers.tag_serializers import TagSerializer
from apps.users.models import User


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Project.objects.all(),
    )
    assignee = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required=False,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'priority',
            'project',
            'tags',
            'deadline',
            'assignee'
        )

    def validate_name(self, value: str) -> str:
        if len(value) < 10:
            raise serializers.ValidationError(
                "The name of the task couldn't be less than 10 characters"
            )
        return value

    def validate_description(self, value: str) -> str:
        if len(value) < 50:
            raise serializers.ValidationError(
                "The description of the task couldn't be less than 50 characters"
            )
        return value

    def validate_priority(self, value: int) -> int:
        if value not in [val[0] for val in Priority.choices()]:
            raise serializers.ValidationError(
                "The priority of the task couldn't be one of the available options"
            )
        return value

    def validate_project(self, value: Project) -> Project:
        if not Project.objects.filter(name=value.name).exists():
            raise serializers.ValidationError(
                "The project with this name couldn't be found in the database"
            )
        return value

    def validate_tags(self, value: List[Tag]) -> List[Tag]:
        tag_ids = [tag.id for tag in value]
        if not Tag.objects.filter(id__in=tag_ids).count() == len(tag_ids):
            raise serializers.ValidationError(
                "One or more tags couldn't be found in the database"
            )
        return value

    def validate_deadline(self, value: datetime) -> datetime:
        if value < timezone.now():
            raise serializers.ValidationError(
                "The deadline of the task couldn't be in the past"
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        task.tags.set(tags)
        task.save()
        return task

    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tags', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags:
            instance.tags.set(tags)

        instance.save()

        return instance

class TaskDetailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    project = ProjectShortInfoSerializer()
    tags = TagSerializer(many=True)

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Task
        exclude = ('updated_at', 'deleted_at')
from rest_framework import serializers

from projects.models import Project


class ProjectDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"

class AllProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
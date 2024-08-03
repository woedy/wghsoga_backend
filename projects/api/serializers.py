from rest_framework import serializers

from projects.models import Project, ProjectImage, ProjectVideo, ProjectSupporter


class ProjectSupporterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSupporter
        fields = "__all__"
class ProjectVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectVideo
        fields = "__all__"
class ProjectImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectImage
        fields = "__all__"


class ProjectDetailsSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(many=True)
    project_videos = ProjectVideoSerializer(many=True)
    class Meta:
        model = Project
        fields = "__all__"

class AllProjectsSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(many=True)
    project_videos = ProjectVideoSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"
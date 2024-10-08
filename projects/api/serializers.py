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
    project_images = serializers.SerializerMethodField()
    project_videos = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = "__all__"

    
    def get_project_images(self, obj):
        # Fetching only the 'photos' field from the Event Images model
        return obj.project_images.filter(is_archived=False).values_list('image', flat=True)



    def get_project_videos(self, obj):
        # Fetching only the 'videos' field from the Event Videos model
        return obj.project_videos.filter(is_archived=False).values_list('video', flat=True)


class AllProjectsSerializer(serializers.ModelSerializer):
    project_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"



        
    def get_project_image(self, obj):
        project_image = obj.project_images.first()
        if project_image:
            return project_image.image.url
        return None
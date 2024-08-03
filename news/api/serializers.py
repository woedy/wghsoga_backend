from rest_framework import serializers

from accounts.api.serializers import ListAllUsersSerializer
from news.models import News, NewsComment, NewsImage, NewsVideo
from projects.models import Project





class NewsCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsComment
        fields = "__all__"


class NewsVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsVideo
        fields = "__all__"


class NewsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsImage
        fields = "__all__"


class NewsDetailsSerializer(serializers.ModelSerializer):
    news_comments = NewsCommentSerializer(many=True)
    news_images = NewsImageSerializer(many=True)
    news_videos = NewsVideoSerializer(many=True)
    likes = ListAllUsersSerializer(many=True)
    shares = ListAllUsersSerializer(many=True)
    author = ListAllUsersSerializer(many=False)


    class Meta:
        model = News
        fields = "__all__"

class AllNewsSerializer(serializers.ModelSerializer):
    news_comments = NewsCommentSerializer(many=True)
    news_images = NewsImageSerializer(many=True)
    news_videos = NewsVideoSerializer(many=True)
    likes = ListAllUsersSerializer(many=True)
    shares = ListAllUsersSerializer(many=True)
    author = ListAllUsersSerializer(many=False)

    class Meta:
        model = News
        fields = "__all__"
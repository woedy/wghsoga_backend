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
    news_images = serializers.SerializerMethodField()
    news_videos = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    shares = ListAllUsersSerializer(many=True)
    likes = ListAllUsersSerializer(many=True)
    author = ListAllUsersSerializer(many=False)


    class Meta:
        model = News
        fields = "__all__"

    
    def get_comment_count(self, obj):
        return obj.news_comments.count()
    
    
    def get_like_count(self, obj):
        return obj.likes.count()

    
    def get_share_count(self, obj):
        return obj.shares.count()
    

    
    def get_news_images(self, obj):
        # Fetching only the 'photos' field from the news Images model
        return obj.news_images.filter(is_archived=False).values_list('image', flat=True)


    
    def get_news_videos(self, obj):
        # Fetching only the 'photos' field from the news news_videos model
        return obj.news_videos.filter(is_archived=False).values_list('video', flat=True)




class AllNewsSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    news_image = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["news_id", "title", 'content', 'like_count', 'share_count', 'comment_count', 'news_image']
        

        
    def get_news_image(self, obj):
        news_image = obj.news_images.first()
        if news_image:
            return news_image.image.url
        return None

    def get_comment_count(self, obj):
        return obj.news_comments.count()
    
    
    def get_like_count(self, obj):
        return obj.likes.count()

    
    def get_share_count(self, obj):
        return obj.shares.count()

    


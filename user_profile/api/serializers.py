from rest_framework import serializers

from user_profile.models import UserProfile, UserInterest


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = "__all__"
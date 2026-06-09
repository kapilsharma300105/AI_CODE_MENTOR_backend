from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username"
    )

    email = serializers.EmailField(
        source="user.email"
    )

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile

        fields = [
            "username",
            "email",
            "bio",
            "avatar",
        ]

    def get_avatar(self, obj):

        if obj.avatar:
            return obj.avatar.url

        return None
    
    from rest_framework import serializers
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
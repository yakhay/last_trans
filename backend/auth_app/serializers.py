from rest_framework import serializers

from .models import CustomUser 


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'photo_profile', 'score', 'win', 'lose', 'ranking', 'total_match']

from rest_framework import serializers
from .models import profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = profile
        fields = ['username', 'password', 'role']

        extra_kwargs = {
            'password': {'write_only': True},
        }

        read_only_fields = ['email']

    def create(self, validated_data):
        return profile.objects.create_user(**validated_data)
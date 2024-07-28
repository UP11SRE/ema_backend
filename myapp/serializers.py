   # file_manager/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File

class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = User
           fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
       


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'size', 'google_drive_id', 'owner', 'shared_with', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def create(self, validated_data):
      google_drive_id = validated_data.get('google_drive_id')
      file, created = File.objects.get_or_create(
          google_drive_id=google_drive_id,
          defaults={**validated_data, 'owner': self.context['request'].user}
      )
      if not created:
          # If the file already exists, update its attributes except for the owner
          file.name = validated_data.get('name', file.name)
          file.size = validated_data.get('size', file.size)
          file.save()
      return file

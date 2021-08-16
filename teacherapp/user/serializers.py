from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        depth = 1

class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        user = self.context["request"].user
        if user.is_teacher == True:
            instance = Session.objects.create(**validated_data)
            return instance
    

class GradeSerializer(ModelSerializer):
    class Meta:
        model = Greade
        fields = "__all__" 
        depth = 1

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        depth = 1

class SocialSerializer(ModelSerializer):
    class Meta:
        model = SocialHandles
        fields = "__all__"
        depth = 1
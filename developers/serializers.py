from projects.serializers import ProjectSerializer
from rest_framework import serializers
from .models import Profile, Skill
from rest_framework_simplejwt.tokens import RefreshToken


class ProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField(read_only=True)
    projects = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def get_skills(self, obj):
        skills = obj.skill_set.all()
        serializer = SkillSerializer(skills, many=True)
        return serializer.data
    
    def get_projects(self, obj):
        projects = obj.project_set.all()
        serializer = ProjectSerializer(projects, many=True)
        return serializer.data


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'
    
class CustomerSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj.user)
        return str(token.access_token)
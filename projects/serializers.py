from developers.models import Profile
from rest_framework import serializers
from .models import Project, Review, Tag
from rest_framework_simplejwt.tokens import RefreshToken

class ProjectSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    reviewers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    
    def get_tags(self, obj):
        serializer = TagSerializer(obj.tags, many=True)
        return serializer.data
    
    def get_owner(self, obj):
        serializer = CustomerSerializer(obj.owner, many=False)
        return serializer.data
    
    def get_reviewers(self, obj):
        return obj.reviewers


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def get_owner(self, obj):
        serializer = CustomerSerializer(obj.owner, many=False)
        return serializer.data
        

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
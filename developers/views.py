from projects.models import Project, Tag
from developers.serializers import CustomerSerializer, ProfileSerializer
from django.contrib.auth.models import User
from developers.models import Profile, Skill
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
import json

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        customer = Profile.objects.get(user=user)
        serializer = CustomerSerializer(customer).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getDevelopers(request):
    query = request.query_params.get('q')
    if query is None:
        developers = Profile.objects.all()
        serializer = ProfileSerializer(developers, many=True)
        return Response(serializer.data)
    else:
        developers = Profile.objects.filter(Q(name__icontains=query) | Q(username__icontains=query))
        serializer = ProfileSerializer(developers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getDeveloper(request, pk):
    developer = Profile.objects.get(username=pk)
    serializer = ProfileSerializer(developer, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    
    try:
        user = User.objects.create(
            username = data['username'],
            email= data['email'],
            password = make_password(data['password'])
        )

        developer = Profile.objects.create(
            user = user,
            name = data['name'],
            username = data['username'],
            email= data['email']
        )

        serializer = CustomerSerializer(developer, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'Пользователь с таким именем уже зарегистрирован'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateUser(request):
    data = request.data
    try:
        profile = Profile.objects.get(id=int(data['id']))
        profile.user.username = data['username']
        profile.name = data['name']
        profile.email = data['email']
        profile.username = data['username']
        profile.location = data['location']
        profile.short_intro = data['intro']
        profile.bio = data['bio']
        if len(data['picture']) != 0:
            profile.profile_image = data['picture']
        profile.social_github = data['github']
        profile.social_vk = data['vk']
        profile.social_linkedin = data['linkedin']
        profile.social_youtube = data['youtube']
        profile.social_website = data['website']
        profile.save()
        profile.user.save()
        serializer = CustomerSerializer(profile, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'Ошибка с сервером, попробуйте позже'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addSkill(request):
    data = request.data
    try:
        profile = Profile.objects.get(id=int(data['id']))
        Skill.objects.create(
            owner = profile,
            name = data['name'],
            description = data['description']
        )
        serializer = CustomerSerializer(profile, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'Ошибка с сервером, попробуйте позже'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addProject(request):
    data = request.data
    try:
        profile = Profile.objects.get(id=int(data['id']))
        project = Project.objects.create(
            owner = profile,
            title = data['title'],
            description = data['description'],
            demo_link = data['demo_link'],
            source_link = data['source_link']
        )
        if len(data['picture']) != 0:
            project.featured_image = data['picture']
        
        if len(data['tags']) != 0:
            tags = json.loads(data['tags'])
            for el in tags:
                tag = Tag.objects.get(name=el['value'])
                project.tags.add(tag)
        
        project.save()
    except:
        message = {'detail':'Ошибка с сервером, попробуйте позже'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



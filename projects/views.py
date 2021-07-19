from developers.models import Profile
from projects.serializers import ProjectSerializer, TagSerializer
from projects.models import Project, Review, Tag
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# Create your views here.


@api_view(['GET'])
def getProjects(request):
    query = request.query_params.get('q')
    if query is None:
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    else:
        projects = Project.objects.filter(title__icontains=query)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getProject(request, name):
    project = Project.objects.get(title=name)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addReview(request):
    data = request.data
    try:
        developer = Profile.objects.get(username=data['username'])
        project = Project.objects.get(title=data['title'])
        Review.objects.create(
            owner = developer,
            project = project,
            body = data['body'],
            value = data['vote']
        )
        project.getVoteCount()
        return Response("Review was created")
    except:
        message = {'detail':'Ошибка с сервером, попробуйте позже'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getTags(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)
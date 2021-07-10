from projects.serializers import ProjectSerializer
from projects.models import Project
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
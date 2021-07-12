from projects.serializers import ProjectSerializer
from developers.serializers import ProfileSerializer
from developers.models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q

# Create your views here.


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





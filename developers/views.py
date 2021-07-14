from developers.serializers import CustomerSerializer, ProfileSerializer
from developers.models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

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





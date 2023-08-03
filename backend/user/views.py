from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, CreateUserSerializer
from api.permissions import IsAdminPermission

User = get_user_model()

# retrieving user details given an access token
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
retrieve_user_view = UserDetailView.as_view()


# retrieving access groups for the authenticated user
class AccessGroupsView(APIView):
    def get(self, request, format=None):
        user = request.user
        groups = user.groups.all()
        group_names = [group.name for group in groups]
        return Response({'groups': group_names})
    
access_groups_view = AccessGroupsView.as_view()


# create new user
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [IsAdminPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({'detail': 'User created successfully.'}, status=201)
    
create_user_view = CreateUserView.as_view()
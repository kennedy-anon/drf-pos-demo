from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, CreateUserSerializer, UserPermissionsSerializer
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

        return Response({'detail': 'User created successfully.', "user_id": user.id,}, status=201)
    
create_user_view = CreateUserView.as_view()


# granting and revoking permissions
class UserPermissionsView(generics.CreateAPIView):
    serializer_class = UserPermissionsSerializer
    permission_classes = [IsAdminPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user_id']
        groups_to_add = serializer.validated_data.get('group_ids', [])
        groups_to_remove = serializer.validated_data.get('remove_group_ids', [])
        is_active = serializer.validated_data.get('is_active', None)

        if groups_to_add:
            user.groups.add(*groups_to_add)
        if groups_to_remove:
            user.groups.remove(*groups_to_remove)
        if is_active is not None:
            user.is_active = is_active
            user.save()

        return Response({'detail': 'User status updated.'}, status=200)
    
set_user_permissions_view = UserPermissionsView.as_view()

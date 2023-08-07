from django.db import IntegrityError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer, ListUsersSerializer, ChangePasswordSerializer, UserChangePasswordSerializer
from api.permissions import IsAdminPermission, IsCashier

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


# granting and revoking permissions and updating user detail
class UpdateUserView(generics.CreateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAdminPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user_id']
        groups_to_add = serializer.validated_data.get('group_ids', [])
        groups_to_remove = serializer.validated_data.get('remove_group_ids', [])
        is_active = serializer.validated_data.get('is_active', None)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')

        if groups_to_add:
            user.groups.add(*groups_to_add)
        if groups_to_remove:
            user.groups.remove(*groups_to_remove)
        if is_active is not None:
            user.is_active = is_active
        if username is not None:
            try:
                user.username = username
                user.save()
            except IntegrityError as e:
                return Response({'detail': 'Username already exists.'}, status=400)
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
            
        user.save()

        return Response({'detail': 'User details updated.'}, status=200)
    
update_user_view = UpdateUserView.as_view()


# listing users
class ListUsersView(generics.ListAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        return User.objects.all()
    
list_users_view = ListUsersView.as_view()


# delete user
class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminPermission]

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'detail': 'User deleted successfully.'}, status=200)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)
        
delete_user_view = DeleteUserView.as_view()


# view for admin to change users password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAdminPermission]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.kwargs['user_id']  # Get the user ID from the URL
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        # Change the password
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=200)
    
change_password_view = ChangePasswordView.as_view()


# view for user to change his / her password
class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsCashier]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response({'detail': 'Incorrect old password.'}, status=400)
        
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({'new_password': e.messages}, status=400)
        
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=200)
    
change_my_password_view = UserChangePasswordView.as_view()
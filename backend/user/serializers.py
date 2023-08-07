from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password

# serializing the user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name'
        ]


# for creating a new user
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields =[
            'username', 'password', 'email', 'first_name', 'last_name'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    

# for updating user detail
class UpdateUserSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    remove_group_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, allow_null=True, many=True)
    is_active = serializers.BooleanField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


# listing users
class ListUsersSerializer(serializers.ModelSerializer):
    user_groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'user_groups', 'is_active', 'username', 'email', 'first_name', 'last_name']

    def get_user_groups(self, user):
        groups = user.groups.all()
        return [{'id': group.id, 'name': group.name} for group in groups]


# change password, admin priviledge
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


# for user to change his/ her password
class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
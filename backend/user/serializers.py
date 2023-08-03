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
    

# for setting & removing permissions & deactivating account
class UserPermissionsSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    remove_group_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, allow_null=True, many=True)
    is_active = serializers.BooleanField(required=False)
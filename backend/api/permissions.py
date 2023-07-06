from rest_framework.permissions import BasePermission

# permission to: add products details
class IsAdminPermission(BasePermission):
    message = 'You do not have permission to do that.'

    def has_permission(self, request, view):
        # check if the user belongs to the SystemAdmin
        return request.user.groups.filter(name='SystemAdmin').exists()
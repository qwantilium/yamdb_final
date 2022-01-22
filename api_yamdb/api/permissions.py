from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_administrator or request.user.is_staff
        return False


class ReadOnly(permissions.BasePermission):
    '''Access is granted to unauth users if the request method is get'''

    def has_permission(self, request, view):
        return request.method == 'GET'


class AuthorModerAdminOrReadOnly(permissions.BasePermission):
    '''
    Checking for authentication if the request method is not GET
    Сhecking if the user is the author of the object
    '''
    def has_permission(self, request, view):
        return (request.method == 'GET'
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_administrator
            or request.user.is_moderator
            or request.user.is_staff
        )

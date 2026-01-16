from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
    # allow authenticated users to list/create by default; rely on object perms
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
        return True
    owner_fields = ('created_by', 'user', 'owner')
    for f in owner_fields:
        if hasattr(obj, f):
            return getattr(obj, f) == request.user
    # fallback: allow staff
    return request.user and request.user.is_staff

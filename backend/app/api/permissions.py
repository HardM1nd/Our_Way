from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
 """ 
Custom permission: allow full access to owners, read-only for others. Assumes viewset has
.get_object()
returning model with
created_by
or
user
"""
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


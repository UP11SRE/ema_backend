   # file_manager/permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerOrShared(BasePermission):
       def has_object_permission(self, request, view, obj):
           return obj.owner == request.user or request.user in obj.shared_with.all()
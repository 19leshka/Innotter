from django.http import HttpRequest
from rest_framework.permissions import BasePermission

from post.models import Post


class IsPostOwner(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Post) -> bool:
        return obj.owner == request.user

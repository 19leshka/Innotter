from django.http import HttpRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS


class PageAccessPermission(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: dict) -> bool:
        return (
                request.method in SAFE_METHODS or
                obj.owner == request.user
                or request.user.is_staff
        )


class IsPageOwner(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: dict) -> bool:
        return obj.owner == request.user

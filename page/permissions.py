from django.http import HttpRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS

from page.models import Page


class PageAccessPermission(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Page) -> bool:
        return (
                request.method in SAFE_METHODS or
                obj.owner == request.user
                or request.user.is_staff
        )


class IsPageOwner(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Page) -> bool:
        return obj.owner == request.user

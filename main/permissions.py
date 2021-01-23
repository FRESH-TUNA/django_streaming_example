from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

class OnlyList(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        if view.action == 'list': return True
        else:
            return bool(request.user and request.user.is_authenticated)

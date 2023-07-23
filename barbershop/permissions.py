from rest_framework.permissions import BasePermission
from barber_shop.models import Schedules


class PermissionBarber(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        id = request.data.get('id')
        schedule = Schedules.objects.filter(pk=id, chosen_barber=user).exists()
        return bool(user and user.is_authenticated and schedule)

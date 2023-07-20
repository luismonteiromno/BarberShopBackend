from rest_framework import routers

from users.views import UserViewset
from barber_shop.views import CompanysViewSet, SchedulesViewset

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', UserViewset, basename='users')
router.register(r'companys', CompanysViewSet, basename='companys')
router.register(r'schedules', SchedulesViewset, basename='schedules')

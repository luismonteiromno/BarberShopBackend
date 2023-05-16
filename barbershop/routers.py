from rest_framework import routers

from users.views import UserViewset

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', UserViewset, basename='users')

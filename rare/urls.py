from django.conf.urls import include
from django.urls import path
from rareapi.views import Tags
from rareapi.views import Posts
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tags', Tags, 'tag')
router.register(r'posts', Posts, 'post')

urlpatterns = [
    path('', include(router.urls)),
    # path('register', register_user),
    # path('login', login_user),
    # path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

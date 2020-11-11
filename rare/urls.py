from django.conf.urls import include
from django.urls import path
from rareapi.views import Tags, PostTags
from rareapi.views import register_user, login_user
from rest_framework import routers
from rareapi.views import Categories, Posts, Users


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'tags', Tags, 'tag')
router.register(r'post_tags', PostTags, 'posttag')
router.register(r'posts', Posts, 'post')
router.register(r'users', Users, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

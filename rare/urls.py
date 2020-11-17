from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rareapi.views import Tags, PostTags
from rareapi.views import register_user, login_user
from rareapi.views import Posts
from rareapi.views import Comments
from rest_framework import routers
from rareapi.views import Categories, Posts, Users, Reactions


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'tags', Tags, 'tag')
router.register(r'comments', Comments, 'comment')
router.register(r'post_tags', PostTags, 'posttag')
router.register(r'posts', Posts, 'post')
router.register(r'users', Users, 'user')
router.register(r'reactions', Reactions, 'reaction')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

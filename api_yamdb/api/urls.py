from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, Signup, TitleViewSet, Token, UserViewSet)


router = SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('v1/auth/signup/', Signup.as_view(), name='signup'),
    path('v1/auth/token/', Token.as_view(), name='token'),
    path('v1/', include(router.urls)),
]

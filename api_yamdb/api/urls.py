from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet, TokenView,
                    UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('v1/auth/token/', TokenView.as_view(), name='token')
]

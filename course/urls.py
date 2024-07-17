from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import (CourseApiView, TopicApiView, VideoApiView, CommentApiView, LikeDislikeApiView,
                    RegisterApiView,EmailMessageApiView)

from rest_framework import routers

router = routers.SimpleRouter()
router.register('courses', CourseApiView, basename='index')
router.register('topics', TopicApiView)
router.register('videos', VideoApiView)
router.register('comments', CommentApiView)
router.register('likes', LikeDislikeApiView)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/register/', RegisterApiView.as_view()),
    path('api/v1/send-email/',EmailMessageApiView.as_view()),

    path('api-auth/', include('rest_framework.urls')),

    # swager
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

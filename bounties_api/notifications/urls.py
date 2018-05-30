from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from notifications import views


router = DefaultRouter()

router.register(r'user/(?P<user_id>\d+)', views.NotificationViewSet, 'user_notifications')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^(?P<notification_id>\d+)/view/$', views.NotificationViewed.as_view()),
    url(r'^user/(?P<user_id>\d+)/view_all/$', views.NotificationViewAll.as_view()),
]

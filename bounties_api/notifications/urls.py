from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from notifications import views


router = DefaultRouter()

router.register(r'activity/user/(?P<user_id>\d+)', views.NotificationActivityViewSet, 'user_activity_notifications')
router.register(r'push/user/(?P<user_id>\d+)', views.NotificationPushViewSet, 'user_push_notifications')
router.register(r'transaction/user/(?P<user_id>\d+)', views.TransactionViewSet, 'user_transaction_notifications')


urlpatterns = [
    url(r'^activity/user/(?P<user_id>\d+)/view_all/$', views.NotificationActivityViewAll.as_view()),
    url(r'^push/user/(?P<user_id>\d+)/view_all/$', views.NotificationPushViewAll.as_view()),
    url(r'^(?P<notification_id>\d+)/view/$', views.NotificationViewed.as_view()),
    url(r'^', include(router.urls)),
]

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from notifications import views


router = DefaultRouter()

router.register(r'activity/user/(?P<public_address>\w+)', views.NotificationActivityViewSet, 'user_activity_notifications')
router.register(r'push/user/(?P<public_address>\w+)', views.NotificationPushViewSet, 'user_push_notifications')
router.register(r'transaction/user/(?P<public_address>\w+)', views.TransactionViewSet, 'user_transaction_notifications')


urlpatterns = [
    url(r'^activity/user/(?P<public_address>\w+)/view_all/$', views.NotificationActivityViewAll.as_view()),
    url(r'^push/user/(?P<public_address>\w+)/view_all/$', views.NotificationPushViewAll.as_view()),
    url(r'^activity/(?P<notification_id>\d+)/view/$', views.NotificationViewed.as_view()),
    url(r'^push/(?P<notification_id>\d+)/view/$', views.NotificationViewed.as_view()),
    url(r'^transaction/(?P<transaction_id>\d+)/view/$', views.TransactionViewed.as_view()),
    url(r'^', include(router.urls)),
]

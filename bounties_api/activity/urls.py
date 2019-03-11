from rest_framework.routers import DefaultRouter
from activity import views


router = DefaultRouter()

router.register(r'^all', views.ActivityViewSet, base_name='activity')
# router.register(r'^bounty/(?P<bounty_id>\d+)/comment', views.BountyComments, 'bounty_comments')

urlpatterns = router.urls

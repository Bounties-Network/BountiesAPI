from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from std_bounties import views


router = DefaultRouter()

router.register(r'bounty', views.BountyViewSet)
router.register(r'fulfillment', views.FulfillmentViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^stats/(?P<address>\w+)/$', views.BountyStats.as_view()),
    url(r'^user/(?P<address>\w+)/$', views.UserProfile.as_view()),
    url(r'^leaderboard/issuer/$', views.LeaderboardIssuer.as_view()),
    url(r'^leaderboard/fulfiller/$', views.LeaderboardFulfiller.as_view()),
    url(r'^token/$', views.Tokens.as_view())
]

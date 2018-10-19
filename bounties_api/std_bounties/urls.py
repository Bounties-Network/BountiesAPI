from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from std_bounties import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Bounties Network API",
      default_version='v1',
      description="Bounties Network API documentation",
      terms_of_service="https://explorer.bounties.network/tos",
      contact=openapi.Contact(email="contact@bounties.network"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

router.register(r'^bounty/draft', views.DraftBountyWriteViewSet)
router.register(r'^bounty', views.BountyViewSet)
router.register(r'^fulfillment', views.FulfillmentViewSet)
router.register(r'^category', views.CategoryViewSet)
router.register(r'^reviews', views.ReviewsViewSet, 'user_reviews')
router.register(r'^bounty/(?P<bounty_id>\d+)/comment',
    views.BountyComments, 'bounty_comments')

urlpatterns = [
    url(r'^leaderboard/issuer/$', views.LeaderboardIssuer.as_view()),
    url(r'^leaderboard/fulfiller/$', views.LeaderboardFulfiller.as_view()),
    url(r'^token/$', views.Tokens.as_view()),
    url(r'^bounty/(?P<bounty_id>\d+)/fulfillment'
        '/(?P<fulfillment_id>\d+)/review/$',
        views.SubmissionReviews.as_view()),
    url(r'^$', swagger_view),
    url(r'^swagger.json$', open_api_view),
    url(r'^', include(router.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

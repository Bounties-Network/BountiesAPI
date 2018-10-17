from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from std_bounties import views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import (
    SwaggerUIRenderer,
    OpenAPIRenderer
)

swagger_view = get_schema_view(
    title='Bounties API',
    renderer_classes=[SwaggerUIRenderer]
)

open_api_view = get_schema_view(
    title='Bounties API',
    renderer_classes=[OpenAPIRenderer]
)


router = DefaultRouter()

router.register(r'^bounty/draft', views.DraftBountyWriteViewSet)
router.register(r'^bounty', views.BountyViewSet)
router.register(r'^fulfillment', views.FulfillmentViewSet)
router.register(r'^category', views.CategoryViewSet)
router.register(r'^reviews', views.ReviewsViewSet, 'user_reviews')
router.register(r'^bounty/(?P<bounty_id>\d+)/comment', views.BountyComments, 'bounty_comments')

urlpatterns = [
    url(r'^leaderboard/issuer/$', views.LeaderboardIssuer.as_view()),
    url(r'^leaderboard/fulfiller/$', views.LeaderboardFulfiller.as_view()),
    url(r'^token/$', views.Tokens.as_view()),
    url(r'^bounty/(?P<bounty_id>\d+)/fulfillment/(?P<fulfillment_id>\d+)/review/$', views.SubmissionReviews.as_view()),
    url(r'^$', swagger_view),
    url(r'^swagger.json$', open_api_view),
    url(r'^', include(router.urls)),
]

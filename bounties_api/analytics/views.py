from datetime import datetime, date
import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from analytics.filters import BountiesTimelineFilter
from .serializers import BountiesTimelineSerializer
from .models import BountiesTimeline


class TimelineBounties(APIView):
    def get(self, request):
        queryset = request.query_params.copy()
        since = queryset.get('since', "")
        until = queryset.get('until', datetime.now().date())

        try:
            since_date = datetime.strptime(since, "%Y-%m-%d").date()

            if type(until) is not date:
                until_date = datetime.strptime(until, "%Y-%m-%d").date()
            else:
                until_date = until

            if type(since_date) is date and type(until_date) is date:
                queryset['until'] = until_date
                queryset['since'] = since_date

                bounties_timeline = BountiesTimelineFilter(queryset,
                                                           BountiesTimeline.objects.all(),
                                                           request=request)


                serialized = BountiesTimelineSerializer(bounties_timeline.qs, many=True, context={'request': request})

                return Response(serialized.data)
        except ValueError:
            pass

        res = {"error": 400, "message": "The fields since & until needs being formated as YYYY-MM-DD"}
        return Response(json.dumps(res), status=status.HTTP_200_OK)





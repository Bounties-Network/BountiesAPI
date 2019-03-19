from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
from bounties.utils import extractInParams, limitOffsetParams, sqlGenerateOrList, dictfetchall
from std_bounties.serializers import LeaderboardFulfillerSerializer
from std_bounties.queries import LEADERBOARD_FULFILLER_QUERY


class LeaderboardFulfiller(APIView):
    @staticmethod
    def get(request):
        sql_param = ''
        platform_in = extractInParams(request, 'platform', 'platform__in')
        startIndex, endIndex = limitOffsetParams(request)
        if platform_in:
            sql_param = 'AND ( '
            sql_param += sqlGenerateOrList(
                'fulfillment.\"platform\"', len(platform_in), '=')
            sql_param += ' OR '
            sql_param += sqlGenerateOrList('bounty.\"platform\"',
                                           len(platform_in), '=')
            sql_param += ' )'
        platform_in = platform_in + platform_in

        formatted_query = LEADERBOARD_FULFILLER_QUERY.format(sql_param)
        cursor = connection.cursor()
        cursor.execute(formatted_query, platform_in)
        query_result = dictfetchall(cursor)
        narrowed_result = query_result[startIndex: endIndex]
        serializer = LeaderboardFulfillerSerializer(narrowed_result, many=True)
        return JsonResponse({'count': len(query_result), 'results': serializer.data}, safe=False)

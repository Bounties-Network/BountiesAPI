from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from bounties.utils import extractInParams, limitOffsetParams, sqlGenerateOrList, dictfetchall
from std_bounties.serializers import LeaderboardIssuerSerializer
from std_bounties.queries import LEADERBOARD_ISSUER_QUERY, LEADERBOARD_ISSUER_QUERY_TOKENS


class LeaderboardIssuer(APIView):
    @staticmethod
    def get(request):
        sql_param = ''
        platform_in = extractInParams(request, 'platform', 'platform__in')
        token_in = extractInParams(request, 'token', 'token__in')
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
        if token_in:
            sql_param += 'AND ( '
            sql_param += "bounty.\"token_contract\" = \'"
            sql_param += token_in[0]
            sql_param += "\')"
            formatted_query = LEADERBOARD_ISSUER_QUERY_TOKENS.format(sql_param)
        else:
            formatted_query = LEADERBOARD_ISSUER_QUERY_TOKENS.format(sql_param)

        cursor = connection.cursor()
        cursor.execute(formatted_query, platform_in)
        query_result = dictfetchall(cursor)
        narrowed_result = query_result[startIndex: endIndex]
        serializer = LeaderboardIssuerSerializer(narrowed_result, many=True)
        return JsonResponse({'count': len(query_result), 'results': serializer.data}, safe=False)

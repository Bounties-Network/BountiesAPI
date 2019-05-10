from django.db.models import Count
from django.http import JsonResponse
from rest_framework.views import APIView
from std_bounties.models import Bounty, Token
from std_bounties.serializers import TokenSerializer


class Tokens(APIView):
    @staticmethod
    def get(self):
        token_qs = {}
        result = []
        token_to_append = {}
        token_count = {}
        token_count = Bounty.objects.values(
            'token_symbol', 'token_contract', 'token_decimals').annotate(
            count=Count('token_symbol')).order_by('-count')
        for bounty in token_count:
            token_to_append = {}
            token_to_append.update(bounty)
            token_qs = Token.objects.filter(symbol=bounty['token_symbol'])
            if token_qs.count() > 0:
                serializer = TokenSerializer(token_qs, many=True)
                token_to_append['token'] = serializer.data
            else:
                token_to_append['token'] = []
            result.append(token_to_append)
        return JsonResponse(result, safe=False)

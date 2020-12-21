from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status

from .core_service import parse_all_chart, update_record, get_all_chart, filter_chart

@api_view(['GET'])
def update_chart(request):
    response = parse_all_chart()
    for record in response:
        update_record(record['auth'], record['song'], record['pos'])
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_chart(request):
    if request.GET:
        response = filter_chart(request.GET)
        return Response(response)
    else:
        response = get_all_chart()
        return Response(response, status=status.HTTP_200_OK)


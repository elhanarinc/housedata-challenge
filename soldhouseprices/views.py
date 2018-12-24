from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from soldhouseprices.lib import timeseries, histogram
import json


@require_http_methods(['GET'])
def index(request):
    return JsonResponse({'result': 'OK'})


@require_http_methods(['GET'])
def get_time_series(request):
    body = json.loads(request.body)
    response_data = timeseries.timeseries_helper(body)
    return JsonResponse(response_data, safe=False)


@require_http_methods(['GET'])
def get_histogram(request):
    body = json.loads(request.body)
    response_data = histogram.histogram_helper(body)
    return JsonResponse(response_data, safe=False)

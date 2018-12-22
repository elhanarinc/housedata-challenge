from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from soldhouseprices.lib import timeseries, histogram

import json


@csrf_exempt
def index(request):
    return JsonResponse({'result': 'OK'})


@csrf_exempt
def get_time_series(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        response_data = timeseries.timeseries_helper(body)
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'result': 'Only GET requests are allowed for Time Series Data!'})


@csrf_exempt
def get_histogram(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        print(body)
        return JsonResponse({'result': 'Histogram'})
    else:
        return JsonResponse({'result': 'Only GET requests are allowed for Histogram Data!'})

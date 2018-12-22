from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from soldhouseprices.models import HouseData

import json


@csrf_exempt
def index(request):
    return JsonResponse({'result': 'OK'})


@csrf_exempt
def get_time_series(request):
    if request.method == 'GET':
        # body = json.loads(request.body)
        # print(body)
        get_filtered_houses()
        return JsonResponse({'result': 'Time Series'})
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


def get_filtered_houses():
    house_data = HouseData.objects.filter(postcode='SA68 0ZA')
    for house in house_data:
        print(house.transaction_unique_identifier)
        print(house.postcode)
        print(house.price)


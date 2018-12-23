from soldhouseprices.models import HouseData
from django.db.models import Avg
import datetime
import math
import logging

logger = logging.getLogger(__name__)

months = {
    'January':      1,
    'February':     2,
    'March':        3,
    'April':        4,
    'May':          5,
    'June':         6,
    'July':         7,
    'August':       8,
    'September':    9,
    'October':      10,
    'November':     11,
    'December':     12
}

response_data = [
    {
        'name': 'Detached',
        'data': []
    },
    {
        'name': 'Semi-detached',
        'data': []
    },
    {
        'name': 'Terraced',
        'data': []
    },
    {
        'name': 'Flat',
        'data': []
    },
    {
        'name': 'Other',
        'data': []
    }
]


def timeseries_helper(request):
    logger.info('%s comes to "/timeseries" endpoint', str(request))

    if 'postcode' not in request or request['postcode'] == '':
        logger.error('No postcode has found on request!')
        return {'result': 'No postcode has found on request!'}

    req_postcode = request['postcode']

    if 'from_date' not in request or request['from_date'] == '':
        logger.info('No from_date has found on request, taking today as from_date!')
        now = datetime.datetime.now()
        from_date = datetime.date(now.year, now.month, now.day)
    else:
        from_date = request['from_date']
        from_date = str(from_date).split(' ')
        from_date_month = int(months[from_date[0]])
        from_date_year = int(from_date[1])
        from_date = datetime.date(from_date_year, from_date_month, 1)

    if 'to_date' not in request or request['to_date'] == '':
        logger.info('No to_date has found on request, taking today as to_date!')
        now = datetime.datetime.now()
        to_date = datetime.date(now.year, now.month, now.day)
    else:
        to_date = request['to_date']
        to_date = str(to_date).split(' ')
        to_date_month = int(months[to_date[0]])
        to_date_year = int(to_date[1])
        to_date = datetime.date(to_date_year, to_date_month, 1)

    house_data = HouseData.objects.values('property_type', 'date_of_transfer')\
        .annotate(average_price=Avg('price'))\
        .filter(postcode=req_postcode, date_of_transfer__range=(from_date, to_date))\
        .order_by('date_of_transfer')

    logger.info('%s records has been found.', str(len(house_data)))

    for daily_data in house_data:
        daily_data_array = [daily_data['date_of_transfer'], math.floor(daily_data['average_price'])]
        if daily_data['property_type'] == 'D':
            response_data[0]['data'].append(daily_data_array)
        elif daily_data['property_type'] == 'S':
            response_data[1]['data'].append(daily_data_array)
        elif daily_data['property_type'] == 'T':
            response_data[2]['data'].append(daily_data_array)
        elif daily_data['property_type'] == 'F':
            response_data[3]['data'].append(daily_data_array)
        elif daily_data['property_type'] == 'O':
            response_data[4]['data'].append(daily_data_array)

    return response_data

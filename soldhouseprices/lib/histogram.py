from soldhouseprices.models import HouseData
from calendar import monthrange
import datetime
import math
import logging

logger = logging.getLogger(__name__)

months = {
    'january':      1,
    'february':     2,
    'march':        3,
    'april':        4,
    'may':          5,
    'june':         6,
    'july':         7,
    'august':       8,
    'september':    9,
    'october':      10,
    'november':     11,
    'december':     12
}

BIN_NUMBER = 8


def histogram_helper(request):
    logger.info('%s comes to "/histogram" endpoint', str(request))

    if 'postcode' not in request or request['postcode'] == '':
        logger.error('No postcode has found on request!')
        return {'result': 'No postcode has found on request!'}

    req_postcode = request['postcode']

    if 'date' not in request or request['date'] == '':
        logger.info('No date has found on request, taking today as date!')
        now = datetime.datetime.now()
        selected_date_start = datetime.date(now.year, now.month, 1)
        selected_date_end = datetime.date(now.year, now.month, now.day)
    else:
        selected_date = request['date']
        selected_date = str(selected_date).split(' ')

        if str(selected_date[0]).lower() not in months:
            logger.error('Month of the date object has not been found!')
            return {'result': 'Month of the date object has not been found!'}

        selected_date_month = int(months[str(selected_date[0]).lower()])

        try:
            selected_date_year = int(selected_date[1])
        except:
            logger.error('Cannot parse Year of date object into a number!')
            return {'result': 'Cannot parse Year of date object into a number!'}

        month_last_date = monthrange(selected_date_year, selected_date_month)[1]

        selected_date_start = datetime.date(selected_date_year, selected_date_month, 1)
        selected_date_end = datetime.date(selected_date_year, selected_date_month, month_last_date)

    logger.info('Start Date: %s - End Date: %s', str(selected_date_start), str(selected_date_end))

    house_data = HouseData.objects.values('price')\
        .filter(postcode=req_postcode, date_of_transfer__range=(selected_date_start, selected_date_end))\
        .order_by('price')

    logger.info('%s records has been found.', str(len(house_data)))

    histogram_data = []
    if len(house_data) != 0:
        min_price_data = house_data[0]['price']
        max_price_data = house_data[len(house_data)-1]['price']

        bin_range = math.ceil((max_price_data - min_price_data) / BIN_NUMBER)

        while min_price_data < max_price_data:
            bucket = {
                'label': str(min_price_data) + ' € - ' + str(min_price_data + bin_range) + ' €',
                'min': min_price_data,
                'max': min_price_data + bin_range,
                'count': 0
            }
            histogram_data.append(bucket)
            min_price_data += bin_range

        for house in house_data:
            for bucket in histogram_data:
                if is_inside(house['price'], bucket):
                    bucket['count'] += 1

    return histogram_data


def is_inside(price, bucket):
    if bucket['min'] <= price <= bucket['max']:
        return True
    return False

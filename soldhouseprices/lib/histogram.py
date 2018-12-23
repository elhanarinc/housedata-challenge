import datetime
import math
from calendar import monthrange
from soldhouseprices.models import HouseData


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

BIN_NUMBER = 8


def histogram_helper(request):
    req_postcode = request['postcode']
    selected_date = request['date']

    if selected_date:
        selected_date = str(selected_date).split(' ')

        selected_date_month = int(months[selected_date[0]])
        selected_date_year = int(selected_date[1])

        month_last_date = monthrange(selected_date_year, selected_date_month)[1]

        selected_date_start = datetime.date(selected_date_year, selected_date_month, 1)
        selected_date_end = datetime.date(selected_date_year, selected_date_month, month_last_date)
    else:
        now = datetime.datetime.now()
        selected_date_start = datetime.date(now.year, now.month, 1)
        selected_date_end = datetime.date(now.year, now.month, now.day)

    house_data = HouseData.objects.values('price')\
        .filter(postcode=req_postcode, date_of_transfer__range=(selected_date_start, selected_date_end))\
        .order_by('price')

    histogram_data = []
    if len(house_data) != 0:
        min_price_data = house_data[0]['price']
        max_price_data = house_data[len(house_data)-1]['price']

        bin_range = math.ceil((max_price_data - min_price_data) / BIN_NUMBER)

        while min_price_data < max_price_data:
            bucket = {
                'label': str(min_price_data) + '€ - ' + str(min_price_data + bin_range) + '€',
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

        for bucket in histogram_data:
            print(bucket)

    return histogram_data


def is_inside(price, bucket):
    if bucket['min'] <= price <= bucket['max']:
        return True
    return False
